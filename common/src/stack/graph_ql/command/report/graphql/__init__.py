# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@
# 

import re
import stack.commands
from stack.db import db
from pprint import pprint

class command(stack.commands.report.command):
	pass

class Command(command):
	"""
	Output the GraphQL schema definition (SDL) generated with the database schema.
	"""

	def get_table_names(self):
		"""Returns a list of the table names in the database"""
		db.execute("SHOW tables")

		table_names = []
		for table in db.fetchall():
			table_names.append(list(table.values())[0])

		return table_names

	def get_table_description(self, table_name):
		"""
		return list of descriptions
		{
			'Default': None,
			'Extra': 'auto_increment',
			'Field': 'id',
			'Key': 'PRI',
			'Null': 'NO',
			'Type': 'int(11)'
		}
		"""
		db.execute(f'DESCRIBE {table_name}')

		return db.fetchall()


	def get_table_references(self, table_name):
		"""
		return list of references
		{
			'column_name': 'node_id',
			'referenced_column_name': 'ID',
			'referenced_table_name': 'nodes',
			'table_name': 'scope_map'
		}
		"""
		db.execute(f'SELECT table_name, referenced_table_name, column_name, referenced_column_name from information_schema.KEY_COLUMN_USAGE where table_name="{table_name}"')

		return db.fetchall()

	def get_scalar_value(self, string, required = False):
		scalars = {
			'varchar': 'String',
			'text': 'String',
			'int': "Int",
			'enum': 'String', # TODO: Create enum here
		}

		check_string = string.lower()

		for scalar in scalars:
			if scalar in check_string:
				ext = '!' if required else ''
				return f"{scalars[scalar]}{ext}"

	def generate_type_fields(self, table_name, description, reference):
		fields = []
		for field in description:
			field_name = self.camel_case_it(field['Field'])
			field_type = self.get_scalar_value(field['Type'], field['Null'] == 'NO')
			fields.append((field_name, field_type))

		return fields

	def generate_type_field_strings(self, field_types):
		"""Returns field types "Id: String" """
		fields = map(lambda field: "  {}: {}".format(*field), field_types)
		return "\n".join(fields)

	def generate_query_type_field(self, table_name):
		return (self.camel_case_it(table_name), self.pascal_case_it(table_name))

	def generate_query_type_field_strings(self, query_types):
		"""Returns query field types "nodes: [Nodes]" """
		return "  {}: [{}]".format(*query_types)

	def camel_case_it(self, string, delimeter = "_"):
		"""Return string in camelCase form"""
		string = "".join([word.capitalize() for word in string.split(delimeter)])
		return string[0].lower() + string[1:]

	def pascal_case_it(self, string, delimeter = "_"):
		"""Return string in PascalCase form"""
		return "".join([word.capitalize() for word in string.split(delimeter)])

	def generate_types(self):

		gql_types = []
		for table_name in self.get_table_names():
			description = self.get_table_description(table_name)
			reference = self.get_table_description(table_name)
			gql_types.append({
				self.pascal_case_it(table_name): self.generate_type_fields(table_name, description, reference)
			})

		types_list = []
		for gql_type in gql_types:
			for type_name, type_values in gql_type.items():
				types_list.append("type %s {\n%s\n}\n" % (type_name, self.generate_type_field_strings(type_values)))

		return types_list

	def generate_queries(self):

		gql_types = []
		for table_name in self.get_table_names():
			gql_types.append(self.generate_query_type_field(table_name))

		query_list = ["extend type Query {",]
		for gql_type in gql_types:
			query_list.append(self.generate_query_type_field_strings(gql_type))

		query_list.append("}")
		return query_list

	def run(self, params, args):

		self.beginOutput()

		self.addOutput(self, "\n".join(self.generate_types()))
		self.addOutput(self, "\n".join(self.generate_queries()))

		self.endOutput(padChar='', trimOwner=True)