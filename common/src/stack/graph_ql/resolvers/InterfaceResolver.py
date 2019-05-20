# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
from stack.graph_ql.connections import db
from collections import namedtuple

class Interface(graphene.ObjectType):
    id: graphene.Int()
    # host = graphene.Field(lambda: Host)
    mac = graphene.String()
    ip = graphene.String()
    netmask = graphene.String()
    gateway = graphene.String()
    name = graphene.String()
    device = graphene.String()
    subnet = graphene.String()
    module = graphene.String()
    vlanid = graphene.Int()
    options = graphene.String()
    channel = graphene.String()
    main = graphene.Int()