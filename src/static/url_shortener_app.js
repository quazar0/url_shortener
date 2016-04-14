// var $notify;   // = $( ".notify" );
var $errormsg;

var $long_url;
var $short_url;
var $shorten_result;
var $shorten_result_section;
var $expand_result;
var $expand_result_section;

var $test_cmd_result_section;
var $test_redirect_result_section;
var testUrlList;



function updateErrorMsg( msg ) {
   $errormsg.text( msg ).addClass( "msg-highlight" );
   if ( msg )
      $errormsg.show();
   else
      $errormsg.hide();
   setTimeout( function() { $errormsg.removeClass( "msg-highlight" ); }, 1500 );
}


function shortenUrl( event ) {
   console.debug( "shortenUrl(): called" );
   // console.log( "shortenUrl(): called; data=" + event.data );
   updateErrorMsg( '' );
   $expand_result_section.hide();
   $shorten_result_section.hide();
   $shorten_result.html( "" );
   var api_url = SCRIPT_ROOT + '/api/shorten';     // setup data for restful api call
   //console.debug( "shortenUrl(): api_url=" + api_url );
   var long_url = $long_url.val();
   var api_args = { 'url': long_url }
   console.debug( "shortenUrl(): url=" + api_args.url );
   // make api call to shorten url
   $.getJSON( api_url, api_args )
      .done(   function( data, status, xhr ) {    // successful
                  console.debug( "shortenUrl() done; status=" + status );
                  var html_val = '<a id="short_a" href="' + data.url + '">' + data.url + '</a>';
                  $shorten_result.html( html_val );
                  $shorten_result_section.show();
               }
      )
      .fail(   function( xhr, status, error ) {
                  console.error( "shortenUrl() fail; status=" + status + ", err=" + error );
                  console.error( "shortenUrl() fail; resp='" + xhr.responseText + "'" );
                  var msg = error;
                  if ( xhr.responseText )
                     msg = "ERROR: " + xhr.responseText
                  updateErrorMsg( msg );
               }
      );
}


function expandUrl( event ) {
   console.log( "expandUrl(): called" );
   updateErrorMsg( '' );
   $shorten_result_section.hide();
   $expand_result_section.hide();
   $expand_result.html( "" );
   var api_url = SCRIPT_ROOT + '/api/expand';     // setup data for restful api call
   var short_url = $short_url.val();
   var api_args = { 'url': short_url }
   console.log( "expandUrl(): url=" + api_args.url );
   // make api call to expand url
   $.getJSON( api_url, api_args )
      .done(   function( data, status, xhr ) {    // successful
                  //console.log( "expandUrl() done; status=" + status );
                  //dlen = data.length;
                  var html_val = '<a href="' + data.url + '">' + data.url + '</a>';
                  $expand_result.html( html_val );
                  $expand_result_section.show();
               }
      )
      .fail(   function( xhr, status, error ) {
                  console.log( "expandUrl() fail; status=" + status + ", err=" + error );
                  console.log( "expandUrl() fail; resp='" + xhr.responseText + "'" );
                  var msg = error;
                  if ( xhr.responseText )
                     msg = "ERROR: " + xhr.responseText
                  updateErrorMsg( msg );
               }
      );
}


// *********************************************************
// Testing code
// *********************************************************

function runInvalidCmd() {
   console.log( "runInvalidCmd(): called" );
   updateErrorMsg( '' );
   $test_cmd_result_section.hide();
   $test_cmd_result.html( "" );
   var cmd = $( '#invalid_cmd' ).val();
   var api_url = SCRIPT_ROOT + '/api/' + cmd;     // setup data for restful api call
   var api_args = { 'url': "invalid_cmd_test_url" }
   console.log( "runInvalidCmd(): cmd=" + cmd + ", url=" + api_args.url );
   // make api call to invalid cmd
   $.getJSON( api_url, api_args )
      .done(   function( data, status, xhr ) {    // successful
                  //console.log( "runInvalidCmd() done; status=" + status );
                  //dlen = data.length;
                  //var html_val = '<a href="' + data.url + '">' + data.url + '</a>';
                  console.log( "runInvalidCmd() fail; resp='" + xhr.responseText + "'" );
                  $test_cmd_result.html( "Should have gotten an error!" );
                  $test_cmd_result_section.show();
                  updateErrorMsg( "No error returned.  Error was expected." );
               }
      )
      .fail(   function( xhr, status, error ) {
                  console.log( "runInvalidCmd() correct (error); status=" + status + ", err=" + error );
                  console.log( "runInvalidCmd() correct (error); resp='" + xhr.responseText + "'" );
                  var msg = error;
                  if ( xhr.responseText )
                     msg = xhr.responseText
                  //updateErrorMsg( msg );
                  $test_cmd_result.html( "Proper error returned: " + msg );
                  $test_cmd_result_section.show();
               }
      );
}


function completeRedirectTest( i ) {
   console.debug( "completeRedirectTest(): i=" + i );
   //console.debug( "completeRedirectTest(): SCRIPT_ROOT=" + SCRIPT_ROOT );

   var $short_a = $( '#short_a' );
   //console.dir( $short_a );
   if ( ! $short_a.length ) {
      console.error( "completeRedirectTest(): short_a not found" );
      return;
   }
   var shortUrl = $short_a.text();
   //console.dir( shortUrl );
   console.debug( "completeRedirectTest(): full short-url=" + shortUrl );
   if ( ! shortUrl ) {
      console.error( "completeRedirectTest(): short_url is blank" );
      return;
   }
   iPos = shortUrl.lastIndexOf( '/' );
   shortUrl = SCRIPT_ROOT + shortUrl.slice( iPos );
   console.debug( "completeRedirectTest(): short-url=" + shortUrl );

   var p0 = $( "<p></p>" ).text( "Test URL: " + $long_url.val() );
   $test_redirect_result_section.append( p0 );

   // test the redirect on the shortened URL
   $.getJSON( shortUrl )
      .done(   function( data, status, xhr ) {    // successful
                  console.debug( "completeRedirectTest() done; status=" + status );
                  var p = $( "<p></p>" ).text( data.url );
                  $test_redirect_result_section.append( p );
               }
      )
      .fail(   function( xhr, status, error ) {
                  console.debug( "completeRedirectTest() fail; status=" + status + ", err=" + error );
                  console.debug( "completeRedirectTest() fail; resp='" + xhr.responseText + "'" );
                  var msg = "&lt;reason unknown&gt;";
                  if ( error ) {
                     //console.debug( "completeRedirectTest() found error; error='" + error + "'" );
                     msg = error;
                  }
                  if ( xhr.responseText ) {
                     //console.debug( "completeRedirectTest() found respText; text='" + xhr.responseText + "'" );
                     msg = xhr.responseText
                  }
                  msg = "<b>ERROR:</b> " + msg;
                  var p = $( "<p></p>" ).html( msg );
                  $test_redirect_result_section.append( p );
               }
      );

   //var ev = Document.CustomEvent( "test" );
   var ev = { "data" : -1 }
   ev.data = 1 + i;
   startRedirectTest( ev );     // run test on next url
}


function initiateRedirectTest( i, url ) {
   console.debug( "initiateRedirectTest(): i=" + i + ", long-url=" + url );
   $long_url.val( url );
   shortenUrl();
   var checkExist = setInterval(
      function() {
         if ( $( '#short_a' ).length ) {
            console.debug( "Found short_a anchor" );
            clearInterval( checkExist );
            completeRedirectTest( i );
         }
      }, 100);   // check every 100ms
}


function startRedirectTest( event ) {
   i = event.data;
   var url = testUrlList[ i ];
   if ( ! url ) {
      console.info( "startRedirectTest(): all tests complete" );
      return;
   }
   console.debug( "startRedirectTest(): i=" + i + ", long-url=" + url );
   initiateRedirectTest( i, url );
   return;
}


// *********************************************************
// end of testing code
// *********************************************************

function initMainPage() {
   updateErrorMsg( '' );

   $long_url  = $( 'input#long_url'  );
   $short_url = $( 'input#short_url' );

   $shorten_result = $( '#shorten_result' );
   $expand_result  = $( '#expand_result'  );
   $shorten_result_section = $( '#shorten_result_section' );
   $expand_result_section  = $( '#expand_result_section'  );

   $( '#shorten_button' ).on( 'click', shortenUrl );
   $( '#expand_button'  ).on( 'click',  expandUrl );
   $long_url .on( "change", shortenUrl );
   $short_url.on( "change",  expandUrl );

   $shorten_result_section.hide();
   $expand_result_section.hide();

   $( '#test_cmd_div' ).hide();
   $( '#test_redirect_div' ).hide();

   // *** temporary testing code ***

   //$( '#test_cmd_div' ).show();
   //$( '#test_cmd_button' ).on( 'click', runInvalidCmd );
   //$test_cmd_result = $( '#test_cmd_result' );
   //$test_cmd_result_section = $( '#test_cmd_result_section' );
   //$test_cmd_result_section.hide();

   //$( '#test_redirect_div' ).show();
   //$test_redirect_result_section = $( '#test_redirect_result_section' );
   //$( '#test_redirect_button' ).on( 'click', 0, startRedirectTest );
   //testUrlList = [ "http://www.google.com/", "http://www.yahoo.com/", "http://www.gmail.com/" ];
}

