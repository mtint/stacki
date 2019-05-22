# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from collections import namedtuple

class Box(graphene.ObjectType):
    id: graphene.Int()
    name = graphene.String()
    # os = graphene.Field(lambda: Os)
    # pallets = graphene.List(lambda: Pallet)

class Query:
	boxes = graphene.Field()