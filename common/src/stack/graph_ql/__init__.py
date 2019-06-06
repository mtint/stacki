# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from pathlib import Path
import importlib


resolvers = Path("resolvers")
resolvers = [resolver.stem for resolver in resolvers.glob("*Resolver.py")]
# Queries = [importlib.import_module(f'resolvers.{resolver}').Query for resolver in resolvers]

from stack.graph_ql.resolvers import (
	HostResolver,
	AttributeResolver,
	BoxResolver,
	InterfaceResolver,
	NetworkResolver,
	OSResolver,
	PalletResolver,
)

# TODO: Import all the Queries and Mutations dynamically
# TODO: Filter out duplicate resolvers
# class RootQuery(*Queries, graphene.ObjectType):
class RootQuery(
	HostResolver.Query,
	AttributeResolver.Query,
	BoxResolver.Query,
	InterfaceResolver.Query,
	NetworkResolver.Query,
	OSResolver.Query,
	PalletResolver.Query,
	graphene.ObjectType,
):
		pass


schema = graphene.Schema(query=RootQuery)
