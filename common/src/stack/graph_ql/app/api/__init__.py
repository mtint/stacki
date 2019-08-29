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
import asyncio
import requests
import os
import json

from . import models

type_defs = load_schema_from_path(
    "./api/schema/"
)


query = QueryType()

@query.field("list_host")
def resolve_nodes(*_):
    response = requests.post(HASURA_GRAPHQL_URL, headers=headers, json={"query": list_host_query}).json()
    result, errors = [response.get('data'), response.get('errors')]
    if errors:
        raise Exception(errors)
        #raise Exception(errors.get('message'))

    return result['nodes']

@query.field("access")
def resolve_nodes(*_):
    response = requests.post(HASURA_GRAPHQL_URL, headers=headers, json={"query": list_host_query})
    result = response.json().get('data')
    raise Exception(result)
    return result

schema = make_executable_schema(type_defs, [query])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema)

