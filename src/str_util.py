__author__ = 'jnelson <jsn0.list@gmail.com>'

import logging
import string
#from sys_globals  import APP
#import traceback

log = logging.getLogger( "url_shortener_app" )

# //////////////////////////////////////
# RFC 1738 includes this list of characters for a URL:
#
# safe  = $ 36,  - 45,   _  95,  . 46,  + 43
# extra = ! 33,  * 42,  "'" 39,  ( 40,  ) 41,  ',' 44
#
# Here are the characters we use:
base_string_extras = "_-.$()!',+*"   # len = 11
base_string = string.digits + string.ascii_letters + base_string_extras   # len = 10 + 52 + 11 = 73


def int2str( iInt, iBase=64 ) -> str:
   '''Converts the given integer to a string in the given base.

   :param iInt: the integer to convert
   :type  iInt: int_
   :param iBase: the base to use to do the conversion; max = ``73``; default = ``64``
   :type  iBase: int_

   :returns: [str_] the converted value

   This function supports up to base 73.  But be careful using anything above base 64 in a URL.
   Above base 64, these characters will be used::

      '.'  '$'  '('  ')'  '!'  "'"  ','  '+'  '*'

   If you wish to convert the string back into an integer using the Python :func:`int` function, do
   not use a base over 36.

   .. _int: http://docs.python.org/library/stdtypes.html#numeric-types-int-float-long-complex
   '''
   if iBase > 73 or iBase < 2:
      return None

   if iInt < 0:
      return '-' + int2str( -iInt, iBase )
   else:
      (d, m) = divmod( iInt, iBase )
      ch = base_string[ m ]
      if d == 0:
         return ch
      return int2str( d, iBase ) + ch


def str2int( sInt, iBase=64 ) -> int:
   '''Parses the given string and converts it to an integer using the given base.

   :param sInt: the string to convert
   :type  sInt: str_
   :param iBase: the base to use to do the conversion; max = ``73``; default = ``64``
   :type  iBase: int_

   :returns: [int_] the converted integer

   This function supports up to base 73.  For base 64, in addition to all alphanumeric characters, the characters '_'
   and '-' are used.  For anything above base 64, these characters are recognized (in numeric order, least significant
   *digit* first)::

      '.'  '$'  '('  ')'  '!'  "'"  ','  '+'  '*'

   '''
   if iBase > 73 or iBase < 2:
      log.critical( "Invalid base argument; base must be between 2 and 73; base=%s", str(iBase) )
      return None

   if iBase <= 36:
      return int( sInt, iBase )

   conv_string = base_string[:iBase]      # get the conversion characters just for the given base
   #return sum( conv_string.index(c) * pow(iBase, p) for p, c in enumerate(reversed(sInt)) )
   iRetval = 0
   for c in sInt:                         # loop thru each character of the input string
      if c not in conv_string:            # if it is not a valid char, then log an error
         log.critical( "Invalid character in input string argument for given base; char=%s, str=%s, base=%s",
                       str(c), str(sInt), str(iBase) )
         return None
      i = conv_string.index( c )          # convert this char to its numeric value
      iRetval = ( iRetval * iBase ) + i   # shift the digits over in the current int, and add the new number

   return iRetval

