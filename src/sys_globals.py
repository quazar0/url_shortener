
from flask import Flask
from flask_restful  import Api

__author__ = 'jnelson <jsn0.list@gmail.com>'

APP = Flask( "url_shortener_app" )   # , static_url_path='' )
API = Api( APP )

APP.secret_key = 'x=[loVY>ZW1hcOdAqkC;}!nyfwY7jW'
#APP.config[ 'DEBUG' ] = True
##APP.debug = True

#g_sUrlHost = "localhost:5000"
g_sUrlHost = "jsn9.sytes.net"
g_sUrlPrefix = "http://" + g_sUrlHost + '/'


def init_db_path( path=None ):
   global APP
   if "DB_PATH" not in APP.config:
      if not path:
         import os.path
         path = os.path.join( APP.root_path, 'data', 'url.db' )
      APP.config[ 'DB_PATH' ] = path
   return APP.config[ 'DB_PATH' ]

