# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import stack.commands


class Plugin(stack.commands.Plugin, stack.commands.Command):

	def provides(self):
		return 'basic'

	def run(self, args):
		(hosts, expanded, hashit) = args

		keys      = [ ] 
		host_info = dict.fromkeys(hosts)
		for host in hosts:
			host_info[host] = []

		if expanded:
			# This is used by the MessageQ as a permanent handle on
			# Redis keys. This allows both the networking and names
			# of hosts to change and keeps the mq happy -- doesn't
			# break the status in 'list host'.
			keys.append('id')

		rows = self.graphql(query_string = """
			query hosts($expanded: Boolean!) {
				allHosts {
					id @include(if: $expanded)
					name
					rack
					rank
					appliance
					os
					box
					environment
					osaction
					installaction
				}
			}
			""", variables = {"expanded": expanded})

		for host in rows['allHosts']:
			host_name = host.pop('name')
			host_values = list(host.values())
			if host_name in host_info:
				host_info[host_name].extend(host_values)

		keys.extend(['rack', 'rank',
					 'appliance',
					 'os', 'box',
					 'environment',
					 'osaction', 'installaction'])
		return { 'keys' : keys, 'values': host_info }

