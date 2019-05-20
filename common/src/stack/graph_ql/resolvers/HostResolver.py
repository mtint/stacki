# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.graph_ql import db
from collections import namedtuple

class Host(graphene.ObjectType):
	id: graphene.Int()
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

class Query(graphene.ObjectType):
	all_hosts = graphene.List(Host)

	def resolve_all_hosts(self, info, **kwargs):
		db.execute(
			"""
			select n.id, n.name, n.rack, n.rank, n.comment, n.metadata,
			a.name,	o.name, b.name,
			e.name, bno.name, bni.name
			from nodes n
			left join appliances a   on n.appliance     = a.id
			left join boxes b        on n.box           = b.id
			left join environments e on n.environment   = e.id
			left join bootnames bno  on n.osaction      = bno.id
			left join bootnames bni  on n.installaction = bni.id
			left join oses o	 on b.os            = o.id
			"""
		)
		hosts = db.fetchall()
		Host = namedtuple(
			"Host",
			[
				"id",
				"name",
				"rack",
				"rank",
				"comment",
				"metadata",
				"appliance",
				"os",
				"box",
				"environment",
				"osaction",
				"installaction",
			],
		)
		hosts = [Host(*host) for host in hosts]

		return hosts