# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.graph_ql import db
from collections import namedtuple


class Attribute(graphene.ObjectType):
	scope = graphene.String()
	attr = graphene.String()
	value = graphene.String()
	shadow = graphene.String()
	scope_id = graphene.Int()


class Query:
	all_attributes = graphene.List(Attribute)

	def resolve_all_attributes(self, info, **kwargs):
		db.execute(
		"""
		select * from attributes
		"""
		)
		attributes = db.fetchall()
		Attribute = namedtuple(
				"Attribute", ["scope", "attr", "value", "shadow", "scope_id"]
		)

		attrs = [Attribute(*attr) for attr in attributes]

		return attrs
