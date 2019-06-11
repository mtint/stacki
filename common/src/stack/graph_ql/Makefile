# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@


PKGROOT		= /opt/stack
ROLLROOT	= ../../../..
DEPENDS.DIRS	= resolvers server

include $(STACKBUILD)/etc/CCRules.mk

build:

install::
	mkdir -p $(ROOT)/$(PY.STACK)/stack/graph_ql/resolvers
	mkdir -p $(ROOT)/$(PY.STACK)/stack/graph_ql/server

	$(INSTALL) -m 0644 $(wildcard resolvers/*.py)	$(ROOT)/$(PY.STACK)/stack/graph_ql/resolvers/
	$(INSTALL) -m 0644 $(wildcard server/*.py)	$(ROOT)/$(PY.STACK)/stack/graph_ql/server/
	$(INSTALL) -m 0644 $(wildcard pylib/graph_ql/*.py)	$(ROOT)/$(PY.STACK)/stack/graph_ql/

clean::