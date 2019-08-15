# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import (
    ObjectType,
    QueryType,
    SubscriptionType,
    gql,
    make_executable_schema,
    load_schema_from_path,
)
from ariadne.asgi import GraphQL
#from stack.db import *
import asyncio

type_defs = load_schema_from_path(
    #"/opt/stack/lib/python3.7/site-packages/stack/graph_ql/schema/"
    "./api/schema/"
)

schema = make_executable_schema(type_defs, [])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema)

