# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import (
    ObjectType,
    QueryType,
    SubscriptionType,
    gql,
    make_executable_schema,
    load_schema_from_path,
)
from ariadne.asgi import GraphQL
from stack.db import *
import asyncio

type_defs = load_schema_from_path(
    "/opt/stack/lib/python3.7/site-packages/stack/graph_ql/schema/"
)

query = QueryType()


@query.field("allHosts")
def resolve_all_hosts(*_):
    database.execute(
        """
		select n.id as id, n.name as name, n.rack as rack, n.rank as rank,
		n.comment as comment, n.metadata as metadata,	a.name as appliance,
		o.name as os, b.name as box, e.name as environment,
		bno.name as osaction, bni.name as installaction
		from nodes n
		left join appliances a   on n.appliance     = a.id
		left join boxes b        on n.box           = b.id
		left join environments e on n.environment   = e.id
		left join bootnames bno  on n.osaction      = bno.id
		left join bootnames bni  on n.installaction = bni.id
		left join oses o	 on b.os            = o.id
		"""
    )

    return database.fetchall()


host = ObjectType("Host")


@host.field("interfaces")
def resolve_host_interfaces(host, *_):
    database.execute(
        f"""
	select i.id as id, n.name as host, mac, ip, netmask, i.gateway,
	i.name as name, device, s.name as subnet, module, vlanid, options, channel, main
	from networks i, nodes n, subnets s
	where i.node = {host['id']} and i.subnet = s.id
	"""
    )

    return database.fetchall()


subscription = SubscriptionType()


@subscription.source("allHosts")
async def host_generator(obj, info):
    while True:
        await asyncio.sleep(1)
        database.execute(
            """
		select n.id as id, n.name as name, n.rack as rack, n.rank as rank,
		n.comment as comment, n.metadata as metadata,	a.name as appliance,
		o.name as os, b.name as box, e.name as environment,
		bno.name as osaction, bni.name as installaction
		from nodes n
		left join appliances a   on n.appliance     = a.id
		left join boxes b        on n.box           = b.id
		left join environments e on n.environment   = e.id
		left join bootnames bno  on n.osaction      = bno.id
		left join bootnames bni  on n.installaction = bni.id
		left join oses o	 on b.os            = o.id
		"""
        )

        yield database.fetchall()


@subscription.field("allHosts")
def host_resolver(obj, info):
    return obj


# TODO: Move out of init
# Dynamic queries
def camel_case_it(string, delimeter="_"):
    """Return string in camelCase form"""
    string = "".join([word.capitalize() for word in string.split(delimeter)])
    return string[0].lower() + string[1:]


def pascal_case_it(string, delimeter="_"):
    """Return string in PascalCase form"""
    return "".join([word.capitalize() for word in string.split(delimeter)])


def find_table_name(field_name, modifier=camel_case_it):
    """Find the non camelCase version of a table name"""
    for table in get_table_names():
        if field_name == modifier(table):
            return table


def get_table_names():
    """
		Returns a list of the table names in the database
		"""

    return database.get_tables()


def get_table_description(table_name):
    """
	return list of descriptions
	"""

    return database.get_columns(table_name)


def get_table_references(table_name):
    """
	return list of references
	"""

    return database.get_foreign_keys(table_name)


def get_table_model(table_name):
    """
	return list of references
	"""
    for model in BaseModel.__subclasses__():
        if model._meta.table.__name__ != table_name:
            continue

        return model


def get_tables_with_references():
    """Returns a list of the table names with referenced tables"""

    table_names = []
    for table in get_table_names():
        if get_table_references(table):
            table_names.append(pascal_case_it(table))

    return table_names


def select_query(obj, info):
    table = get_table_model(info.field_name)

    return table.select()

def nested_select_query(obj, info):
    return getattr(obj, info.field_name)


[
    query.field(camel_case_it(field))(lambda obj, info: select_query(obj, info))
    for field in get_table_names()
]

# 1. get tables with references
tables_names = get_tables_with_references()
# 2. for every table with references I need a new object type
object_types = [ObjectType(field) for field in tables_names]
# 3. in each of those tables I will need to assign a resolver for each field
for object_type in object_types:
    table_name = find_table_name(object_type.name, pascal_case_it)
    for ref in get_table_references(table_name):
        # TODO: Fix This
        field_name = f"{camel_case_it(ref.column)}"
        object_type.field(field_name)(lambda obj, info: nested_select_query(obj, info))

# End dynamic queries

schema = make_executable_schema(type_defs, [query, host, subscription, *object_types])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema)

