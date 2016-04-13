#!/usr/bin/python3

import re

from flask import render_template, jsonify, request, make_response, redirect, send_from_directory
#from flask import flash, redirect, render_template, request, session, url_for
from sys_globals  import APP, g_sUrlPrefix
from data_access  import *

__author__ = "jnelson <jsn0.list@gmail.com>"

reFull = re.compile( r"^https?://" + g_sUrlPrefix + r"(:\d+)?/" )
#reHost = re.compile( g_sUrlPrefix + '/' )


@APP.route( '/' )
def show_main_page():
   #print( str(datetime.now()), "show_main_page(): called" )
   log.debug( "show_main_page(): called" )
   return render_template( 'main.html' )


@APP.route( '/api/shorten', methods=['GET', 'POST'] )
def shorten_url():
   log.debug( "shorten_url(): url_root=%s", request.url_root )
   sLongURL = request.args.get( "url" )
   log.debug( "long-url=%s", repr(sLongURL) )

   sShortPath = get_db_entry( None, sLongURL )     # get short url entry, if it exists
   if sShortPath:                                  # does it already exist? (is it a repeat)
      sShortURL = g_sUrlPrefix + sShortPath        # build url
      return jsonify( url=sShortURL )              # return json

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

   log.debug( "get_expanded_url(): got short path; path=%s", repr(sShortPath) )
   sLongURL = get_db_entry( sShortPath )     # get original (long) url, if it exists
   if sLongURL:                              # was an entry found?
      return ( sLongURL, None )              # yes, so return the original (long) URL
      # jsonify( url=sLongURL )               # yes, so return the original (long) URL
   log.debug( "get_expanded_url(): URL not found; url=%s", repr(sLongURL) )
   return ( None, make_response( ("URL not found", 404, None) ) )


@APP.route( '/api/expand', methods=['GET', 'POST'] )
def expand_url():
   log.debug( "expand_url():url_root=%s", request.url_root )
   sShortURL = request.args.get( "url" )
   log.debug( "called; short-url=" + str(sShortURL) )
   sLongURL, errResp = get_expanded_url( sShortURL )
   if sLongURL:                              # was an entry found?
      return jsonify( url=sLongURL )         # yes, so return the original (long) URL
   return errResp


@APP.route( '/api/<cmd>' )
def handle_invalid_cmd( cmd ):
   log.debug( "handle_invalid_cmd(): Invalid API call; cmd=%s", repr(cmd) )
   return make_response( ("Invalid API call; /api/" + str(cmd), 400, None) )     # abort( 400 )


@APP.route( '/static/<path>', methods=['HEAD', 'OPTIONS', 'GET'] )
def handle_static( path ):
   log.debug( "handle_static(): called; path=%s", str(path) )
   iPos = path.rfind( '/' )
   if iPos < 0:
      filename = path
      directory = "static"
   else:
      iFPos = iPos + 1
      filename = path[ iFPos : ]
      directory = '/'.join( ("static", path[ : iPos ] ) )
   log.debug( "handle_static(): sending file; dir=%s, file=%s", repr(directory), repr(filename) )
   return send_from_directory( directory, filename )


# NOTE: this will also catch /static URLs, if there is not another route for them.
@APP.route('/<path>')
def handle_redirect( path ):
   log.debug( "handle_redirect(): called; path=%s", str(path) )
   log.debug( "url_root=%s", request.url_root )
   log.debug( "url=%s", str(request.url) )
   sLongURL, errResp = get_expanded_url( path )
   if sLongURL:
      log.info( "Redirecting; url=%s", str(sLongURL ) )
      return redirect( sLongURL, 303 )
      #return jsonify( url=sLongURL )
   return errResp


def init_logging():
   #if not APP.debug:
   import logging
   from logging.handlers import SysLogHandler
   syslog_handler = SysLogHandler()
   syslog_handler.setLevel( logging.DEBUG )
   syslog_handler.setFormatter( logging.Formatter(
         '%(levelname)-5s <%(process)5d:%(thread)12x> [%(name)s] %(funcName)s: %(message)s' ) )
   APP.logger.addHandler( syslog_handler )


if __name__ == "__main__":
   init_logging()
   init_database( "jnelson" )
   APP.run( debug=True )

