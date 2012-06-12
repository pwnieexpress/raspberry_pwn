#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: breakpoint.py 194 2007-04-05 15:31:53Z cameron $
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

class breakpoint:
    '''
    Soft breakpoint object.
    '''

    address       = None
    original_byte = None
    description   = None
    restore       = None
    handler       = None

    ####################################################################################################################
    def __init__ (self, address=None, original_byte=None, description="", restore=True, handler=None):
        '''
        @type  address:       DWORD
        @param address:       Address of breakpoint
        @type  original_byte: Byte
        @param original_byte: Original byte stored at breakpoint address
        @type  description:   String
        @param description:   (Optional) Description of breakpoint
        @type  restore:       Boolean
        @param restore:       (Optional, def=True) Flag controlling whether or not to restore the breakpoint
        @type  handler:       Function Pointer
        @param handler:       (Optional, def=None) Optional handler to call for this bp instead of the default handler
        '''

        self.address        = address
        self.original_byte  = original_byte
        self.description    = description
        self.restore        = restore
        self.handler        = handler