# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.graph_ql.resolvers import HostResolver, AttributeResolver

# TODO: Import all the Queries and Mutations dynamically
# TODO: Filter out duplicate resolvers
class RootQuery(HostResolver.Query, AttributeResolver.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=RootQuery)
