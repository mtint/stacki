# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@
#
# @rocks@
# Copyright (c) 2000 - 2010 The Regents of the University of California
# All rights reserved. Rocks(r) v5.4 www.rocksclusters.org
# https://github.com/Teradata/stacki/blob/master/LICENSE-ROCKS.txt
# @rocks@

from itertools import groupby
from operator import itemgetter

class AttrHelper:
	'''
	a mix-in to handle retrieving attributes and returning them in useful ways
	'''

	def getAttr(self, attr):
		return self.getHostAttr('localhost', attr)

	def getHostAttr(self, host, attr):
		for row in self.call('list.host.attr', [host, 'attr=%s' % attr]):
			return row['value']

	def getHostAttrDict(self, host, attr=None):
		"""
		For `host` return all of its attrs in a dictionary
		return {'host1': {'rack': '0', 'rank': '1', ...}, 'host2': {...}, ...}
		This works because multiple attr's cannot have the same name.
		"""

		if type(host) == type([]):
			params = host
		else:
			params = [host]

		if attr:
			params.append(f'attr={attr}')

		return {
			k: {i['attr']: i['value'] for i in v}
			for k, v in groupby(
				self.call('list.host.attr', params),
				itemgetter('host')
			)
		}
