# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
import pymysql
import os
from collections import namedtuple

def connect_db(username="apache", passwd=""):
	passwd = ""
	try:
		file = open("/etc/apache.my.cnf", "r")
		for line in file.readlines():
			if line.startswith("password"):
				passwd = line.split("=")[1].strip()
				break
		file.close()
	except:
		pass

	# Connect to a copy of the database if we are running pytest-xdist
	if "PYTEST_XDIST_WORKER" in os.environ:
		db_name = "cluster" + os.environ["PYTEST_XDIST_WORKER"]
	else:
		db_name = "cluster"

	if os.path.exists("/run/mysql/mysql.sock"):
		db = pymysql.connect(
			db=db_name,
			user=username,
			passwd=passwd,
			host="localhost",
			unix_socket="/run/mysql/mysql.sock",
			autocommit=True,
		)
	else:
		db = pymysql.connect(
			db=db_name,
			host="localhost",
			port=40000,
			user=username,
			passwd=passwd,
			autocommit=True,
		)
	return db.cursor()

db = connect_db()

class Host(graphene.ObjectType):
	id: graphene.Int()
	name = graphene.String()
	rack = graphene.String()
	rank = graphene.String()
	appliance = graphene.String()
	os = graphene.String()
	box = graphene.String()
	environment = graphene.String()
	osaction = graphene.String()
	installaction = graphene.String()
	comment = graphene.String()
	metadata = graphene.String()
	# interfaces = graphene.List(lambda: Interface)

class Query(graphene.ObjectType):
	all_hosts = graphene.List(Host)

	def resolve_all_hosts(self, info, first=None, skip=None, **kwargs):
		db.execute(
			"""
			select n.id, n.name, n.rack, n.rank, n.comment, n.metadata,
			a.name,	o.name, b.name, 
			e.name, bno.name, bni.name 
			from nodes n 
			left join appliances a   on n.appliance     = a.id
			left join boxes b        on n.box           = b.id 
			left join environments e on n.environment   = e.id 
			left join bootnames bno  on n.osaction      = bno.id 
			left join bootnames bni  on n.installaction = bni.id
			left join oses o	 on b.os            = o.id
			"""
		)
		hosts = db.fetchall()
		Host = namedtuple(
			"Host",
			[
				"id",
				"name",
				"rack",
				"rank",
				"comment",
				"metadata",
				"appliance",
				"os",
				"box",
				"environment",
				"osaction",
				"installaction",
			],
		)
		hosts = [Host(*host) for host in hosts]

		if skip:
				hosts = hosts[skip::]

		if first:
				hosts = hosts[:first]

		return hosts

schema = graphene.Schema(query=Query)
