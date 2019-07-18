# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from ariadne import QueryType, ObjectType
from stack.db import db

query = QueryType()

@query.field("allHosts")
def resolve_all_hosts(obj, info):
	db.execute(
		"""
		select n.id as id, n.name as name, n.rack as rack, n.rank as rank,
		n.comment as comment, n.metadata as metadata,	a.name as appliance,
		o.name as os, b.name as box, e.name as environment,
		bno.name as osaction, bni.name as installaction
		from nodes n
		left join appliances a   on n.appliance     = a.id
		left join boxes b        on n.box           = b.id
		left join environments e on n.environment   = e.id
		left join bootnames bno  on n.osaction      = bno.id
		left join bootnames bni  on n.installaction = bni.id
		left join oses o	 on b.os            = o.id
		"""
	)

	return db.fetchall()

host = ObjectType("Host")

@host.field("interfaces")
def resolve_host_interfaces(host, *_):
	db.execute(
	f"""
	select i.id as id, n.name as host, mac, ip, netmask, i.gateway,
	i.name as name, device, s.name as subnet, module, vlanid, options, channel, main
	from networks i, nodes n, subnets s
	where i.node = {host['id']} and i.subnet = s.id
	"""
	)

	return db.fetchall()

resolvers = [query, host]