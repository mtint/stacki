# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import graphene
import pymysql
import os

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


from stack.graph_ql.resolvers import HostResolver, AttributeResolver

# TODO: Import all the Queries and Mutations dynamically
# TODO: Filter out duplicate resolvers
class RootQuery(HostResolver.Query, AttributeResolver.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=RootQuery)
