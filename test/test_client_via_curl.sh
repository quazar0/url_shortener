#!/bin/bash

test_url=${1:-http://www.google.com/}

url_base='http://jsn9.sytes.net'

api_url="$url_base/api"

shorten_api_url="$api_url/shorten"
expand_api_url="$api_url/expand"


function call_get() {
   json=`curl --silent $1`

   py_cmd="print( 'Result:', $json[ 'url' ] )"

   python3 -c "$py_cmd"
}


function expand_url() {
   short_url="$1"
   echo
   echo "Expand url: '$short_url'"
   call_get "${expand_api_url}?url=$short_url"
}


function shorten_url() {
   long_url="$1"
   echo
   echo "Shorten long url: $long_url"
   call_get "${shorten_api_url}?url=$long_url"
}


shorten_url "$test_url"

expand_url "${url_base}/1"
expand_url '/2'
expand_url '3'

