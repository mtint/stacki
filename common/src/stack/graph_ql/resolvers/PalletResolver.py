# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.graph_ql.connections import db
from collections import namedtuple

class Pallet(graphene.ObjectType):
		id: graphene.Int()
		name = graphene.String()
		version = graphene.String()
		release = graphene.String()
		arch = graphene.String()
		os = graphene.String()
		url = graphene.String()
		# boxes = graphene.Field(lambda: Box)