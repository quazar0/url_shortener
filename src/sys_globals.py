
#from flask import Flask
#import logging

__author__ = 'jnelson <jsn0.list@gmail.com>'

#APP = None
#APP = Flask( "url_shortener_app" )   # , static_url_path='' )
#APP.secret_key = 'x=[loVY>ZW1hcOdAqkC;}!nyfwY7jW'

##'%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s'
#APP.debug_log_format = '%(levelname)-5s <%(process)5d:%(thread)12x> [%(name)s] %(funcName)s: %(message)s'

g_sUrlHost = "jsn9.sytes.net"
g_sUrlPrefix = "http://" + g_sUrlHost + '/'

#if not APP.debug:
#from logging.handlers import SysLogHandler
#syslog_handler = SysLogHandler()
#syslog_handler.setLevel( logging.DEBUG )
#syslog_handler.setFormatter( logging.Formatter(
#   '%(levelname)-5s <%(process)5d:%(thread)12x> [%(name)s] %(funcName)s: %(message)s' ) )
#APP.logger.addHandler( syslog_handler )

