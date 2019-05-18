# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene

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