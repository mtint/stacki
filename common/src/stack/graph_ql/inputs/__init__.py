# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene

class HostInput(graphene.InputObjectType):
	name = graphene.String(required=True)
	appliance = graphene.String(required=True)
	rack = graphene.String(required=True)
	rank = graphene.String(required=True)
	box = graphene.String(default_value='default')
	osaction = graphene.String(default_value='default')
	installaction = graphene.String(default_value='default')
	environment = graphene.String(default_value=False)