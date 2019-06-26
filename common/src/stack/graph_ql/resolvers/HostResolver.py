# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from promise import Promise
from promise.dataloader import DataLoader
from stack.db import db
from collections import namedtuple
from stack.graph_ql.inputs import HostInput

class Host(graphene.ObjectType):
	id = graphene.Int()
	name = graphene.String()
	rack = graphene.String()
	rank = graphene.String()
	appliance = graphene.String()
	os = graphene.String()
	box = graphene.String()
	environment = graphene.String()
	osaction = graphene.String()
	installaction = graphene.String()
	comment = graphene.String()
	metadata = graphene.String()
	# interfaces = graphene.List(lambda: Interface)

class Query:
	all_hosts = graphene.List(Host)
 
	def resolve_all_hosts(self, info, **kwargs):
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

		return [Host(**host) for host in db.fetchall()]

class AddHost(graphene.Mutation):
	class Arguments:
		input = HostInput()
	
	ok = graphene.Boolean()

	def mutate(root, info, input):
		# TODO: Reduce number of queries
		db.execute(f'select id from appliances where name="{input["appliance"]}"')
		try:
			appliance = db.fetchall().pop()['id']
		except:
			raise Exception(f'appliance "{input["appliance"]}" is not in the database')

		db.execute(f'select id, os from boxes where name="{input["box"]}"')
		try:
			box_id, os = db.fetchall().pop().values()
		except:
			raise Exception(f'box "{input["box"]}" is not in the database')

		db.execute(f'select name from nodes where name="{input["name"]}"')
		if db.fetchall():
			raise Exception(f'host "{input["name"]}" already exists in the database')

		db.execute('''
				select bn.id as id from
				bootactions ba, bootnames bn
				where ba.bootname = bn.id
				and ba.os = %s
				and bn.name = "%s"
				and bn.type = "install"
				''' % (os, input['installaction']))
		try:
			install_id = db.fetchall().pop()['id']
		except:
			raise Exception(f'installaction "{input["installaction"]}" does not exist')

		db.execute('''
				select bn.id as id from
				bootactions ba, bootnames bn
				where ba.bootname = bn.id
				and bn.name = "%s"
				and bn.type = "os"
				''' % input['installaction'])
		try:
			os_id = db.fetchall().pop()['id']
		except:
			raise Exception(f'osaction "{input["installaction"]}" does not exist')

		environment = None
		if input['environment']:
			db.execute(f'select id from environments where name="{input["name"]}"')
			try:
				environment = db.fetchall().pop()['id']
			except:
				raise Exception(f'environment "{input["environment"]}" is not in the database')

		db.execute('''
			insert into nodes
			(name, rack, rank, installaction, osaction, appliance, box, environment)
			values (%s, %s, %s, %s, %s, %s, %s, %s) 
			''', (
				input['name'],
				input['rack'],
				input['rank'],
				install_id,
				os_id,
				appliance,
				box_id,
				environment,
				)
			)
		print(db.fetchall())
		ok = True
		return AddHost(ok=ok)

class Mutations(graphene.ObjectType):
	add_host = AddHost.Field()