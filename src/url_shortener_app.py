#!/usr/bin/python3

from datetime  import datetime

from flask import render_template

from sys_globals  import APP
#from flask import flash, redirect, render_template, request, session, url_for
#from data_access  import *

__author__ = "jnelson <jsn0.list@gmail.com>"

#user_account.init_user_resources()
#calorie_list.init_calorie_resources()


@APP.route( '/' )
def show_main_page():
   return render_template( 'main.html' )
   #return show_calorie_list_page()


def show_calorie_list_page():
   print( str(datetime.now()), "show_main_page(): called" )
   #APP.logger.debug( "show_main_page(): called" )
   print( str(datetime.now()), "show_main_page(): rendering template for main page" )
   #APP.logger.debug( "show_main_page(): rendering template for calorie_list" )
   #return render_template( 'calorie_list.html', login_user=user, users=user_list )
   return render_template( 'main.html' )



if __name__ == "__main__":
   APP.run( debug=True )

