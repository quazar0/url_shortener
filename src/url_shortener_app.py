#!/usr/bin/python3

import logging
import re

from flask import Flask, render_template, jsonify, request, make_response, redirect, send_from_directory

from sys_globals  import g_sUrlPrefix
from data_access  import *

__author__ = "jnelson <jsn0.list@gmail.com>"

reFull = re.compile( r"^https?://" + g_sUrlPrefix + r"(:\d+)?/" )

APP = Flask( "url_shortener_app" )   # , static_url_path='' )
APP.secret_key = 'x=[loVY>ZW1hcOdAqkC;}!nyfwY7jW'

# '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s'
APP.debug_log_format = '%(levelname)-5s [%(name)s] %(funcName)s: %(message)s'
#APP.debug = True

log = None
sDBUser = None


@APP.route( '/' )
def show_main_page():
   ##print( str(datetime.now()), "show_main_page(): called" )
   #log.debug( "show_main_page(): called" )
   return render_template( 'main.html' )


@APP.route( '/api/shorten', methods=['GET', 'POST'] )
def shorten_url():
   #log.debug( "url_root=%s", request.url_root )
   sLongURL = request.args.get( "url" )
   log.debug( "long-url=%s", repr(sLongURL) )

   sShortPath = get_db_entry( None, sLongURL )     # get short url entry, if it exists
   if sShortPath:                                  # does it already exist? (is it a repeat)
      sShortURL = g_sUrlPrefix + sShortPath        # build url
      return jsonify( url=sShortURL )              # return json

   if not sLongURL.startswith( "http://") and not sLongURL.startswith( "https://"):
      return make_response( ("Invalid URL; must be http: or https:", 400, None) )

   # generate a short URL
   sShortURL = '*** error ***'
   iSeq = add_db_entry( sLongURL )                # insert row in db and get seq number (primary key)
   if iSeq:
      sShortPath = generate_short_url_path( iSeq )
      update_db_entry( iSeq, sShortPath )         # save the entry for it
      sShortURL = g_sUrlPrefix + sShortPath
   return jsonify( url=sShortURL )     # return json


def get_expanded_url( sShortURL ):
   sShortPath = get_url_path( sShortURL )
   if not sShortPath:
      return ( None, make_response( ("Invalid URL; path is missing", 400, None) ) )

   log.debug( "got short path; path=%s", repr(sShortPath) )
   sLongURL = get_db_entry( sShortPath )     # get original (long) url, if it exists
   if sLongURL:                              # was an entry found?
      return ( sLongURL, None )              # yes, so return the original (long) URL
   log.debug( "URL not found; url=%s", repr(sLongURL) )
   return ( None, make_response( ("URL not found", 404, None) ) )


@APP.route( '/api/expand', methods=['GET', 'POST'] )
def expand_url():
   sShortURL = request.args.get( "url" )
   log.debug( "called; short-url=" + str(sShortURL) )
   sLongURL, errResp = get_expanded_url( sShortURL )
   if sLongURL:                              # was an entry found?
      return jsonify( url=sLongURL )         # yes, so return the original (long) URL
   return errResp


@APP.route( '/api/<cmd>' )
def handle_invalid_cmd( cmd ):
   log.debug( "Invalid API call; cmd=%s", repr(cmd) )
   return make_response( ("Invalid API call; /api/" + str(cmd), 400, None) )     # abort( 400 )


@APP.route( '/static/<path:spath>', methods=['HEAD', 'OPTIONS', 'GET'] )
def handle_static( spath ):
   log.debug( "called; path=%s", str(spath) )
   iPos = spath.rfind( '/' )
   directory = APP.root_path + '/'
   if iPos < 0:
      filename = spath
      directory += "static"
   else:
      iFPos = iPos + 1
      filename = spath[ iFPos : ]
      directory += '/'.join( ("static", spath[ : iPos ] ) )
   log.debug( "sending file; dir=%s, file=%s", repr(directory), repr(filename) )
   return send_from_directory( directory, filename )


@APP.route('/<rpath>')
def handle_redirect( rpath ):
   log.debug( "called; rpath=%s", str(rpath) )
   log.debug( "url=%s", str(request.url) )
   sLongURL, errResp = get_expanded_url( rpath )
   if sLongURL:
      log.info( "Redirecting; url=%s", str(sLongURL ) )
      return redirect( sLongURL, 303 )
   return errResp


def init_db_connection( sLogin=None ):
   """Initializes the database connection pool."""
   from sql import SQL
   try:
      SQL.Init( False, sLogin )
   except Exception:
      log.critical( "Failed to init sql layer;", exc_info=True )


@APP.before_first_request
def init_app():
   global log
   log = logging.getLogger( "url_shortener_app" )
   log.setLevel( logging.INFO )   # logging.DEBUG )
   if not APP.debug:
      log_fmt = logging.Formatter( '%(levelname)-5s <%(process)5d:%(thread)12x> [%(name)s] %(funcName)s: %(message)s' )

      str_handler = logging.StreamHandler()
      str_handler.setLevel( logging.DEBUG )
      str_handler.setFormatter( log_fmt )
      log.addHandler( str_handler )

      #from logging.handlers import SysLogHandler
      #syslog_handler = SysLogHandler()
      #syslog_handler.setLevel( logging.DEBUG )
      #syslog_handler.setFormatter( log_fmt )
      #APP.logger.addHandler( syslog_handler )
   else:
      log.setLevel( logging.DEBUG )
      APP.logger.setLevel( logging.DEBUG )

   log.info( "root path: %s", str(APP.root_path) )
   init_db_connection( sDBUser )


#@APP.teardown_appcontext
#def close_db( exc ):
#   db = getattr( g, '_database', None )
#   if db is not None:
#      db.close()


def create_db( sLogin=None ):
   """Create the database table.

   This is used during install.
   """
   from sql import SQL
   print( "create_db() called" )
   with APP.app_context():
      init_db_connection( sLogin )
      db = SQL()
      with APP.open_resource( 'db_schema.sql', mode='r' ) as f:
         sql = f.read( 256 )
      db.Update( sql )



if __name__ == "__main__":
   sDBUser = "jnelson"
   APP.run( debug=True )

