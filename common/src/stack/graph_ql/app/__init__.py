# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import (
    ObjectType,
    QueryType,
		MutationType,
    SubscriptionType,
    gql,
    make_executable_schema,
    load_schema_from_path,
)
from ariadne.asgi import GraphQL
import asyncio
import requests
import os
import json

from . import db

type_defs = load_schema_from_path(
    "./app/schema/"
)


# TODO: Break this out into modules
query = QueryType()
mutations = MutationType()

@query.field("boxes")
def resolve_boxes(*_):
	results, _ = db.run_sql("select id, name, os as os_id from boxes")
	return results

box = ObjectType("Box")
@box.field('os')
def resolve_os_from_id(box, *_):
	result, _ = db.run_sql(f"select id, name from oses where id={box['os_id']}", fetchone = True)
	return result

@query.field("appliances")
def resolve_appliances(*_):
	results, _ = db.run_sql("select id, name, public from appliances")
	return results

@mutations.field("addAppliance")
def resolve_add_appliance(_, info, name, public = "no"):
	# TODO: Fix SQL injection
	# TODO: Maybe make the appliance names unique in the db
	# TODO: Add kickstartable and managed attrs

	cmd = f'INSERT INTO appliances (name, public) VALUES ("{name}", "{public}")'
	db.run_sql(cmd)

	cmd = f'SELECT id, name, public from appliances where name="{name}"'
	result, _ = db.run_sql(cmd, fetchone=True)

	return result

@mutations.field("updateAppliance")
def resolve_update_appliance(_, info, id, name = None, public = None):
	# TODO: Fix SQL injection
	# TODO: Maybe make the appliance names unique in the db
	# TODO: Check if the name collides

	cmd = f'SELECT id, name, public from appliances where id={id}'
	appliance, _ = db.run_sql(cmd, fetchone=True)
	if not appliance:
		raise Exception("No appliance found")

	if not name and not public:
		return appliance

	update_params = []
	if name:
		update_params.append(f'name="{name}"')
		
	if public is not None:
		update_params.append(f'public="{public}"')

	cmd = f'Update appliances set {",".join(update_params)} where id={id}'
	db.run_sql(cmd)

	cmd = f'SELECT id, name, public from appliances where id={id}'
	result, _ = db.run_sql(cmd, fetchone=True)

	return result

@mutations.field("deleteAppliance")
def resolve_delete_appliance(_, info, id):

	cmd = f'DELETE from appliances where id={id}'
	_, affected_rows = db.run_sql(cmd)

	if not affected_rows:
		return False

	return True

schema = make_executable_schema(type_defs, [query, box, mutations])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema)

