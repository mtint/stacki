YUMLIST = \
	MegaCLI storcli \
	stack-command \
	stack-mq \
	stack-pylib \
	stack-storage-config \
	ludicrous-speed \
	foundation-python \
	foundation-python-Flask \
		foundation-python-itsdangerous \
		foundation-python-Werkzeug \
		foundation-python-MarkupSafe \
		foundation-python-Jinja2 \
		foundation-python-Click \
	foundation-python-PyMySQL \
	foundation-python-configparser \
	foundation-python-jsoncomment \
	foundation-python-python-daemon \
		foundation-python-lockfile \
	foundation-python-requests \
		foundation-python-urllib3 \
		foundation-python-chardet \
		foundation-python-certifi \
		foundation-python-idna
	stack-graphql-api \
		foundation-python-ariadne \
			foundation-python-graphql-core \
			foundation-python-typing-extensions


getextrapackages:
	zypper --pkg-cache-dir cache download ipmitool
