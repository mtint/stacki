from ariadne import ObjectType, QueryType, SubscriptionType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from stack.db import db
import asyncio

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql('''
type AddHost {
	"""asdfasdfasdf"""
	ok: Boolean
}

type Host {
	id: Int
	name: String
	rack: String
	rank: String
	appliance: String
	os: String
	box: String
	environment: String
	osaction: String
	installaction: String
	comment: String
	metadata: String
	interfaces: [Interface]
}

type Interface {
	id: Int
	host: String
	mac: String
	ip: String
	netmask: String
	gateway: String
	name: String
	device: String
	subnet: String
	module: String
	vlanid: Int
	options: String
	channel: String
	main: Int
}

type Mutation {
	addHost(appliance: String!, box: String = "default", environment: String = false, installaction: String = "default", name: String!, osaction: String = "default", rack: String!, rank: String!): AddHost
}

type Query {
	allHosts: [Host]
}

type Subscription {
	allHosts: [Host]
}
''')

# Map resolver functions to Query fields using QueryType
query = QueryType()

# Resolvers are simple python functions
@query.field("allHosts")
def resolve_all_hosts(*_):
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

subscription = SubscriptionType()

@subscription.source("allHosts")
async def host_generator(obj, info):
	while True:
		await asyncio.sleep(1)
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

		yield db.fetchall()

@subscription.field("allHosts")
def host_resolver(obj, info):
	return obj

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, [query, host, subscription])

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema, debug=True)
