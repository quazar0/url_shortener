var $notify;   // = $( ".notify" );
var $errormsg;


function updateErrorMsg( msg ) {
   $errormsg.text( msg ).addClass( "msg-highlight" );
   if ( msg )
      $errormsg.show();
   else
      $errormsg.hide();
   setTimeout( function() { $errormsg.removeClass( "msg-highlight" ); }, 1500 );
}

function updateNotifyMsg( msg ) {
   $notify.text( msg ).addClass( "msg-highlight" );
   setTimeout( function() { $notify.removeClass( "msg-highlight" ); }, 1500 );
}


function initMainPage() {
   updateErrorMsg( '' );
   $( '#shorten_button' ).on( 'click', shortenUrl );
   $( '#expand_button'  ).on( 'click',  expandUrl );
   $( '#long_url'  ).on( "change", shortenUrl );
   $( '#short_url' ).on( "change",  expandUrl );
}

