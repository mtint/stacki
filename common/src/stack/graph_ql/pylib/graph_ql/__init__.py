# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import ObjectType, QueryType, SubscriptionType, gql, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from stack.db import db
import asyncio

type_defs = load_schema_from_path("/opt/stack/lib/python3.7/site-packages/stack/graph_ql/schema/")

query = QueryType()

@query.field("allHosts")
def resolve_all_hosts(*_):
	db.execute(
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

	return db.fetchall()

host = ObjectType("Host")

@host.field("interfaces")
def resolve_host_interfaces(host, *_):
	db.execute(
	f"""
	select i.id as id, n.name as host, mac, ip, netmask, i.gateway,
	i.name as name, device, s.name as subnet, module, vlanid, options, channel, main
	from networks i, nodes n, subnets s
	where i.node = {host['id']} and i.subnet = s.id
	"""
	)

	return db.fetchall()

subscription = SubscriptionType()

@subscription.source("allHosts")
async def host_generator(obj, info):
	while True:
		await asyncio.sleep(1)
		db.execute(
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

		yield db.fetchall()

@subscription.field("allHosts")
def host_resolver(obj, info):
	return obj

# TODO: Move out of init
# Dynamic queries
def camel_case_it(string, delimeter = "_"):
	"""Return string in camelCase form"""
	string = "".join([word.capitalize() for word in string.split(delimeter)])
	return string[0].lower() + string[1:]

def pascal_case_it(string, delimeter = "_"):
	"""Return string in PascalCase form"""
	return "".join([word.capitalize() for word in string.split(delimeter)])

def find_table_name(field_name, modifier = camel_case_it):
	"""Find the non camelCase version of a table name"""
	for table in get_table_names():
		if field_name == modifier(table):
			return table

def get_table_names():
	"""Returns a list of the table names in the database"""
	db.execute("SHOW tables")

	table_names = []
	for table in db.fetchall():
		table_names.append(list(table.values())[0])

	return table_names

def get_table_references(table_name):
	"""
	return list of references
	{
		'column_name': 'node_id',
		'referenced_column_name': 'ID',
		'referenced_table_name': 'nodes',
		'table_name': 'scope_map'
	}
	"""
	db.execute(f'SELECT table_name, referenced_table_name, column_name, referenced_column_name from information_schema.KEY_COLUMN_USAGE where table_name="{table_name}"')

	return db.fetchall()
def get_tables_with_references():
	"""Returns a list of the table names with referenced tables"""

	table_names = []
	for table in get_table_names():
		references = get_table_references(table)
		for ref in references:
			if ref['referenced_column_name'] != "NULL":
				table_names.append(pascal_case_it(table))
				break

	return table_names

def select_query(obj, info):
	table_name = info.field_name
	try:
		db.execute(f'DESCRIBE {table_name}')
		table_info = db.fetchall()
	except:
		table_name = find_table_name(info.field_name)
		db.execute(f'DESCRIBE {table_name}')
		table_info = db.fetchall()

	query_string = ", ".join([field["Field"].lower() for field in table_info])
	db.execute(f'select {query_string} from {table_name}')

	return db.fetchall()

def nested_select_query(obj, info):
	referenced_table_name = find_table_name(info.return_type.of_type.name, pascal_case_it)
	parent_table_name = find_table_name(info.parent_type.name, pascal_case_it)
	print(referenced_table_name, parent_table_name)
	try:
		db.execute(f'DESCRIBE {referenced_table_name}')
		table_info = db.fetchall()
	except:
		db.execute(f'DESCRIBE {referenced_table_name}')
		table_info = db.fetchall()

	ref = None
	value = None
	for reference in get_table_references(parent_table_name):
		if reference['referenced_table_name'] == referenced_table_name:
			ref = reference['referenced_column_name']
			value = obj[reference['column_name']]
			break

	query_string = ", ".join([field["Field"].lower() for field in table_info])
	db.execute(f'select {query_string} from {referenced_table_name} where {ref}="{value}"')

	return db.fetchall()

[query.field(camel_case_it(field))(lambda obj, info: select_query(obj, info)) for field in get_table_names()]

# 1. get tables with references
tables_names = get_tables_with_references()
# 2. for every table with references I need a new object type
object_types = [ObjectType(field) for field in tables_names]
# 3. in each of those tables I will need to assign a resolver for each field
for object_type in object_types:
	table_name = find_table_name(object_type.name, pascal_case_it)
	for ref in get_table_references(table_name):
		if not ref['referenced_column_name']:
			continue
		# TODO: Fix This
		field_name = f"{camel_case_it(ref['column_name'])}WithId"
		object_type.field(field_name)(lambda obj, info: nested_select_query(obj, info))

# End dynamic queries

schema = make_executable_schema(type_defs, [query, host, subscription, *object_types])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema)

