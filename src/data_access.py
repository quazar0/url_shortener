
from urllib.parse  import urlsplit

from sql  import SQL
from sys_globals  import APP, g_sUrlHost   # , g_sUrlPrefix
from str_util  import int2str, str2int
#import traceback

__author__ = 'jnelson <jsn0.list@gmail.com>'

log = APP.logger



def get_db_entry( sShortPath, sLongURL=None ):
   #sSelect = sArg = ""
   if sShortPath:
      iUID = str2int( sShortPath )
      sSelect = "SELECT long_url"
      sWhereClause = "WHERE uid = %s"
      tupArg = ( iUID, )
   elif sLongURL:
      sSelect = "SELECT short_url"
      sWhereClause = "WHERE long_url = %s"
      tupArg = ( sLongURL, )
   else:
      return None

   sSQL = sSelect + ' FROM url_list ' + sWhereClause + ';'
   db = SQL( bReadOnly=True )
   tupRow = db.Get( sSQL, tupArg )
   #print( "get_db_entry(): tupRow =", str(tupRow) )
   log.debug( "get_db_entry(): tupRow=%s", str(tupRow) )
   #row = query_db( sSQL, (sArg,), True )
   if not tupRow:
      return None
   sResult = tupRow[ 0 ]   # = rows[0][0]
   return sResult


def add_db_entry( sLongURL ):
   # insert row in db and get seq number (primary key)
   if not sLongURL:
      return None
   db = SQL()
   iUID = db.Insert( (sLongURL,) )
   log.debug( "uid=%s", str(iUID) )
   #print( "add_db_entry(): uid =", str(iUID) )
   return iUID


def update_db_entry( iUID, sShortUrl ):
   sSQL = "UPDATE url_list SET short_url = %s WHERE uid = %s;"
   db = SQL()
   db.Update( sSQL, (sShortUrl, iUID) )


def generate_short_url_path( iSeq ):
   sShort = int2str( iSeq )     # convert to base 64
   if not sShort:
      return None
   return sShort


def init_database( sLogin=None ):
   from db_util  import connect_database
   connect_database( sLogin )


def get_url_path( sURL ):
   tupSplitURL = urlsplit( sURL )
   #print( str(datetime.now()), "expandUrl(): url split; split-url=" + str(tupSplitURL) )
   log.debug( "url split; url=%s", str(tupSplitURL) )
   if tupSplitURL.path:
      sShortPath = tupSplitURL.path
   elif sURL.startswith( g_sUrlHost ):
      # remove hostname, if any, so just the path remains
      #print( "get_url_path(): url host match; match =", repr(g_sUrlHost) )
      log.debug( "url host match; host=%s", repr(g_sUrlHost) )
      iLen = len( g_sUrlHost )
      sShortPath = sURL[ iLen: ]
   else:
      sShortPath = sURL     # looks like it only has the path

   if sShortPath[0] == '/':
      sShortPath = sShortPath[ 1: ]
   return sShortPath

