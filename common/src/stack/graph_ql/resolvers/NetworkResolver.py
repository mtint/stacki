# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.db import db

class Network(graphene.ObjectType):
    id: graphene.Int()
    network = graphene.String()
    address = graphene.String()
    mask = graphene.String()
    gateway = graphene.String()
    mtu = graphene.String()
    zone = graphene.String()
    dns = graphene.String()
    pxe = graphene.String()

class Query:
	pass