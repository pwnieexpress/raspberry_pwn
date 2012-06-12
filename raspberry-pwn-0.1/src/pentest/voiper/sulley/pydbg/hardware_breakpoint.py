#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: hardware_breakpoint.py 194 2007-04-05 15:31:53Z cameron $
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

class hardware_breakpoint:
    '''
    Hardware breakpoint object.
    '''

    address     = None
    length      = None
    condition   = None
    description = None
    restore     = None
    slot        = None
    handler     = None

    ####################################################################################################################
    def __init__ (self, address=None, length=0, condition="", description="", restore=True, slot=None, handler=None):
        '''

        @type  address:     DWORD
        @param address:     Address to set hardware breakpoint at
        @type  length:      Integer (1, 2 or 4)
        @param length:      Size of hardware breakpoint (byte, word or dword)
        @type  condition:   Integer (HW_ACCESS, HW_WRITE, HW_EXECUTE)
        @param condition:   Condition to set the hardware breakpoint to activate on
        @type  description: String
        @param description: (Optional) Description of breakpoint
        @type  restore:     Boolean
        @param restore:     (Optional, def=True) Flag controlling whether or not to restore the breakpoint
        @type  slot:        Integer (0-3)
        @param slot:        (Optional, Def=None) Debug register slot this hardware breakpoint sits in.
        @type  handler:     Function Pointer
        @param handler:     (Optional, def=None) Optional handler to call for this bp instead of the default handler
        '''

        self.address     = address
        self.length      = length
        self.condition   = condition
        self.description = description
        self.restore     = restore
        self.slot        = slot
        self.handler     = handler