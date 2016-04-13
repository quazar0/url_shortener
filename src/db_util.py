
from sql import SQL
from sys_globals  import APP

__author__ = 'jnelson <jsn0.list@gmail.com>'

log = APP.logger


def connect_database( sLogin=None ):
   """Initializes the database connection pool."""
   try:
      SQL.Init( False, sLogin )
   except Exception:
      log.critical( "Failed to init sql layer;", exc_info=True )
   #return db


#@APP.teardown_appcontext
#def close_db( exc ):
#   db = getattr( g, '_database', None )
#   if db is not None:
#      db.close()


def create_db( sLogin=None ):
   """Create the database table.

   This is used during install.
   """
   print( "create_db() called" )
   with APP.app_context():
      connect_database( sLogin )
      db = SQL()
      with APP.open_resource( 'db_schema.sql', mode='r' ) as f:
         sql = f.read( 256 )
      db.Update( sql )

