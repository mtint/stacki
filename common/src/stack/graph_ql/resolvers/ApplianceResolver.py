# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.db import db

class Appliance(graphene.ObjectType):
	id = graphene.Int()
	name = graphene.String()
	public = graphene.String()

class Query(graphene.ObjectType):
	all_appliances = graphene.List(Appliance)

	def resolve_all_appliances(self, info):
		db.execute("""
		select id, name, public
		from appliances
		""")

		return [Appliance(**appliance) for appliance in db.fetchall()]