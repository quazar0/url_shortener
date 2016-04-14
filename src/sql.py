#!/usr/bin/python3

import logging
from time import sleep
from time import time

import psycopg2
import antipool

log = logging.getLogger( "url_shortener_app" )

g_iMAXCONNECTIONS_DEFAULT = 10
g_conn_pool = None


#
class SQL( object ):
   '''This class is responsible for the interface to the underlying SQL database.
   '''
   dictCONFIG = { 'db'  : "maindb"
                , 'user': "url_shortener"
                , 'max_connections': g_iMAXCONNECTIONS_DEFAULT
                }


   def __init__( self, bReadOnly=False ):
      '''SQL constructor, which gets a connection from the connection pool.

      It is possible for this to hang, if the database is swamped.  But it should never throw an
      exception.
      '''
      #log.debug( "called" )
      self.m_conn = self.m_cur = None
      self.m_conn, self.m_cur = SQL.GetConnection( bReadOnly )    # Get DB connection from connection pool
      #if not self.m_conn or not self.m_cur:


   def __del__( self ):
      '''SQL destructor, which closes the cursor and releases the DB connection.
      '''
      try:
         if self.m_cur:
            self.m_cur.close()      # release cursor resources
      finally:
         # Note: Do not close the connection, just release it.
         if self.m_conn:
            self.m_conn.release()   # release connection back to the pool


   def Get( self, sql, tupArgs ) -> tuple:
      result = None
      #log.debug( "called; args=%s, sql=%s", str(tupArgs), repr(sql) )
      try:
         self.m_cur.execute( sql, tupArgs )     # run sql statement
         result = self.m_cur.fetchone()         # get the returned data (as a tuple; one item per column)
         #log.debug( "row fetch'd; result=%s", str(result) )
      except:
         log.critical( "Error during database query; sql=%s, args=%s;", str(sql), str(tupArgs), exc_info=True )
      return result


   def Insert( self, tupArgs ):
      '''Inserts a row into the database, using the given args.

      :returns: [int] the UID (primary key) of the last insert
      '''
      sql = "INSERT INTO url_list ( long_url ) VALUES ( %s ) RETURNING uid;"
      try:
         self.m_cur.execute( sql, tupArgs )     # run sql statement
         self.m_conn.commit()                   # commit the insert
         result = self.m_cur.fetchone()         # get the uid of this insert
         iUID = result[ 0 ]
      except:
         log.critical( "Failure during database insert; sql=%s, args=%s;", str(sql), str(tupArgs), exc_info=True )
         return None
      return iUID


   def Update( self, sql, tupArgs=() ):
      '''Updates the proper row in the database using the given sql and args.
      '''
      #sql = "update url_list set sShortUrl = %s, sLongUrl = %s where uid = %s"   # Build sql statement
      self.m_cur.execute( sql, tupArgs )   # run sql statement
      self.m_conn.commit()


   @staticmethod
   def GetConnection( bReadOnly=False, iTimeout=5 ):
      '''Get DB connection from connection pool.

      :param bReadOnly: flag that indicates if the connection should be ReadOnly (default False; get
                        a ReadWrite connection)
      :type  bReadOnly: :func:`bool <bool>`
      :param iTimeout: if it does not get a connection immediately, this is the amount of time to
                       keep trying (in seconds).
      :type  iTimeout: :func:`int`
      '''
      # default timeout is 5 seconds
      fTimeout = time() + iTimeout
      conn = cur = None
      bGotConnection = False
      while not bGotConnection:
         if time() > fTimeout:
            log.critical( "Timeout occurred during attempt to get connection from connection pool" )
            return (None, None)
         try:
            if g_conn_pool is None:
               log.critical( "Connection pool is missing; DB may not have been initialized" )
               return (None, None)

            if bReadOnly:
               conn = g_conn_pool.connection_ro()
            else:
               conn = g_conn_pool.connection()
            # Read-Committed is the default isolation level in psycopg2.
            #conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
            cur = conn.cursor()
            bGotConnection = True
            #print( "Got connection; conn={0}, cur={1}".format( conn, cur ) )
            log.debug( "Got connection; conn=%s, cur=%s", str(conn), str(cur) )
         except psycopg2.OperationalError as e1:
            sMsg = repr(e1)
            #if sMsg.find("Ident authentication failed") > 0:
            if str(e1).find("FATAL:") >= 0:
               log.critical( "Failed to get connection from connection pool; %s", sMsg )
               raise
            log.warning( "Failed to get a connection from the connection pool; will try again; %s", sMsg )
            sleep(0.5)
         except AttributeError as e2:
            log.warning( "Failed to get a connection from the connection pool; will try again; %s", repr(e2) )
            sleep(0.5)
         except Exception as e3:
            log.critical( "Failed to get a connection from the connection pool; %s", repr(e3) )
            raise
      return conn, cur


   @staticmethod
   def Init( bForce=False, sUserLogin=None ):
      '''Initializes the sql module.

      :param bForce: normally this method will do nothing if it has already been run before; but if
                     this force flag is set True, then the config data will be reloaded and the
                     connection pool will be re-initialized.

      This does the setup for database login, including user name and the max number of connections
      that the connection pool will allow.

      If this method has been run before, then it does nothing, unless the ``bForce`` flag is set
      :data:`True`.

      .. note::
         Postgresql wants the user to be the same as the linux login of the process, unless you
         configure an alias in postgresql.
      '''
      #log.debug( "called; force=%s", str(bForce) )
      # If it is already initialized and the flag is not set to force a re-init, then do nothing.
      if g_conn_pool and not bForce:
         log.debug( "SQL already initialized; nothing to do" )
         return

      sDBName = SQL.dictCONFIG[ 'db'   ]
      if sUserLogin:
         sLogin  = sUserLogin
      else:
         sLogin  = SQL.dictCONFIG[ 'user' ]
      iMaxCon = SQL.dictCONFIG[ 'max_connections' ]

      # setup database connection pool
      SQL.InitConnPool( sDBName, sLogin, iMaxCon )


   @staticmethod
   def InitConnPool( sDatabase, sUser, iMaxConn=g_iMAXCONNECTIONS_DEFAULT ):
      '''Create and init the connection pool.

      :param sDatabase: name of the database
      :param sUser: the database login
      :param iMaxConn: max number of DB connections the pool will allow; note: minimum connections defaults to 5.

      This must be called before any SQL objects can be created.
      '''
      global g_conn_pool

      dictOptions = {    'maxconn': iMaxConn
                    , 'disable_ro': True
                    }

      #logPool = core_logging.getLogger( "core.DBServices.antipool" )
      #dictOptions[ 'debug' ] = logPool

      g_conn_pool = antipool.ConnectionPool( psycopg2,
                                             database=sDatabase,
                                             user=sUser,
                                             options=dictOptions )
      if g_conn_pool is None:
         log.critical( "Failed to get connection pool" )
         raise RuntimeError( "Failed to get connection pool" )

      antipool.initpool( g_conn_pool )


# --- end of SQL class ---

