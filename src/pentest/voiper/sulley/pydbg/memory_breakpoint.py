#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: memory_breakpoint.py 194 2007-04-05 15:31:53Z cameron $
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

import random

class memory_breakpoint:
    '''
    Memory breakpoint object.
    '''

    address     = None
    size        = None
    mbi         = None
    description = None
    handler     = None

    read_count  = 0                                # number of times the target buffer was read from
    split_count = 0                                # number of times this breakpoint was split
    copy_depth  = 0                                # degrees of separation from original buffer
    id          = 0                                # unique breakpoint identifier
    on_stack    = False                            # is this memory breakpoint on a stack buffer?

    ####################################################################################################################
    def __init__ (self, address=None, size=None, mbi=None, description="", handler=None):
        '''
        @type  address:     DWORD
        @param address:     Address of breakpoint
        @type  size:        Integer
        @param size:        Size of buffer we want to break on
        @type  mbi:         MEMORY_BASIC_INFORMATION
        @param mbi:         MEMORY_BASIC_INFORMATION of page containing buffer we want to break on
        @type  description: String
        @param description: (Optional) Description of breakpoint
        @type  handler:     Function Pointer
        @param handler:     (Optional, def=None) Optional handler to call for this bp instead of the default handler
        '''

        self.address     = address
        self.size        = size
        self.mbi         = mbi
        self.description = description
        self.handler     = handler

        self.id          = random.randint(0, 0xFFFFFFFF)    # unique breakpoint identifier
        self.read_count  = 0                                # number of times the target buffer was read from
        self.split_count = 0                                # number of times this breakpoint was split
        self.copy_depth  = 0                                # degrees of separation from original buffer
        self.on_stack    = False                            # is this memory breakpoint on a stack buffer?