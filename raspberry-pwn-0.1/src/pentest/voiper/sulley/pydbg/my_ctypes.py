#!c:\python\python.exe

#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: my_ctypes.py 194 2007-04-05 15:31:53Z cameron $
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
#
# Many thanks to Thomas Heller, for both his efforts in developing the c_types library and for his assistance with
# getting c_types to cooperate with cPickle.
#

'''
@author:       Pedram Amini
@license:      GNU General Public License 2.0 or later
@contact:      pedram.amini@gmail.com
@organization: www.openrce.org
'''

from ctypes import *


########################################################################################################################
def _construct (typ, raw_bytes):
    '''
    This routine is called by _reduce for unmarshaling purposes. The object type is used to instantiate a new object of
    the desired type. The raw bytes are then directly written into the address space of the newly instantiated object
    via the ctypes routines memmove() and addressof().

    @type  typ:       Class object
    @param typ:       The class type of the object we are unmarshaling.
    @type  raw_bytes: Raw bytes (in a string buffer)
    @param raw_bytes: The raw bytes

    @rtype:  Mixed
    @return: Unmarshaled object.
    '''

    obj = typ.__new__(typ)
    memmove(addressof(obj), raw_bytes, len(raw_bytes))

    return obj


########################################################################################################################
def _reduce (self):
    '''
    cPickle will allow an object to marshal itself if the __reduce__ function is defined. Because cPickle is unable to
    handle ctype primitives or the objects derived on those primitives we define this function that later is assigned
    as the __reduce__ method for all types. This method relies on _construct for unmarshaling. As per the Python docs
    __reduce__ must return a tuple where the first element is "A callable object that will be called to create the
    initial version of the object. The next element of the tuple will provide arguments for this callable...". In this
    case we pass the object class and the raw data bytes of the object to _construct.

    @rtype:  Tuple
    @return: Tuple, as specified per the cPickle __reduce__ Python docs.
    '''

    return (_construct, (self.__class__, str(buffer(self))))


########################################################################################################################
c_types = (Structure, c_char, c_byte, c_ubyte, c_short, c_ushort, c_int, c_uint, c_long, c_ulong, c_longlong, \
           c_ulonglong, c_float, c_double, c_char_p, c_wchar_p, c_void_p)


# for each ctype we need to marshal, set it's __reduce__ routine.
for typ in c_types:
    typ.__reduce__ = _reduce