# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import ObjectType, QueryType, MutationType
import app.db as db

query = QueryType()
mutation = MutationType()
group = ObjectType("Group")

@query.field('groups')
def resolve_group(*_):
	results, _ = db.run_sql("SELECT id, name FROM groups")
	return results

@group.field('hosts')
def resolve_host_group(obj, info):
	cmd ="""
		SELECT * FROM nodes INNER JOIN memberships
		on memberships.nodeid=nodes.id WHERE memberships.groupid=%s
		"""
	args = [obj.get('id')]
	results, _ = db.run_sql(cmd, args)
	return results

@mutation.field('addGroup')
def resolve_add_group(_, info, name):
	if name in [group['name'] for group in resolve_group()]:
		raise Exception(f'Group {name} is already defined')

	cmd = 'INSERT INTO groups (name) VALUES(%s)'
	args = (name)
	results, _ = db.run_sql(cmd, args)

	# Get the recently inserted value
	cmd = "SELECT id, name FROM groups WHERE name=%s"
	args = (name, )
	results, _ = db.run_sql(cmd, args, fetchone=True)
	return results

@mutation.field('deleteGroup')
def resolve_delete_group(_, info, name):
	cmd = "DELETE FROM groups WHERE name=%s"
	args = (name, )
	_, affected_rows = db.run_sql(cmd, args)

	# Return false if the db can't find the row to delete
	if not affected_rows:
		return False

	return True

object_types = [group]
