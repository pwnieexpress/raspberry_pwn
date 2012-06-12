#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: pdx.py 194 2007-04-05 15:31:53Z cameron $
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

'''
@author:       Pedram Amini
@license:      GNU General Public License 2.0 or later
@contact:      pedram.amini@gmail.com
@organization: www.openrce.org
'''

from my_ctypes import *
from defines   import *

# macos compatability.
try:
    kernel32 = windll.kernel32
except:
    kernel32 = CDLL("libmacdll.dylib")

class pdx (Exception):
    '''
    This class is used internally for raising custom exceptions and includes support for automated Windows error message
    resolution and formatting. For example, to raise a generic error you can use::

        raise pdx("Badness occured.")

    To raise a Windows API error you can use::

        raise pdx("SomeWindowsApi()", True)
    '''

    message    = None
    error_code = None

    ####################################################################################################################
    def __init__ (self, message, win32_exception=False):
        '''
        '''
        
        self.message    = message
        self.error_code = None

        if win32_exception:
            self.error_msg  = c_char_p()
            self.error_code = kernel32.GetLastError()

            kernel32.FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
                                    None,
                                    self.error_code,
                                    0x00000400,     # MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT)
                                    byref(self.error_msg),
                                    0,
                                    None)


    ####################################################################################################################
    def __str__ (self):
        if self.error_code != None:
            return "[%d] %s: %s" % (self.error_code, self.message, self.error_msg.value)
        else:
            return self.message