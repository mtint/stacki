# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene

from stack.graph_ql.connections import db
from stack.graph_ql.query.host import Query

class Query(Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query)
