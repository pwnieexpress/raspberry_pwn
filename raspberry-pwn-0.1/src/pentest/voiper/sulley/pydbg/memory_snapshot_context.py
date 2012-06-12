#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: memory_snapshot_context.py 194 2007-04-05 15:31:53Z cameron $
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

class memory_snapshot_context:
    '''
    Thread context object, used in memory snapshots.
    '''

    thread_id = None
    context   = None

    ####################################################################################################################
    def __init__ (self, thread_id=None, context=None):
        '''
        @type  thread_id:  Integer
        @param thread_id:  Thread ID
        @type  context:    CONTEXT
        @param context:    Context of thread specified by ID at time of snapshot
        '''

        self.thread_id = thread_id
        self.context   = context