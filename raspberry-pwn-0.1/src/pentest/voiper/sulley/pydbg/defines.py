#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: defines.py 193 2007-04-05 13:30:01Z cameron $
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
# windows_h.py was generated with:
#
#    c:\Python\Lib\site-packages\ctypes\wrap
#    c:\python\python h2xml.py windows.h -o windows.xml -q -c
#    c:\python\python xml2py.py windows.xml -s DEBUG_EVENT -s CONTEXT -s MEMORY_BASIC_INFORMATION -s LDT_ENTRY \
#        -s PROCESS_INFORMATION -s STARTUPINFO -s SYSTEM_INFO -o windows_h.py
#
# Then the import of ctypes was changed at the top of the file to utilize my_ctypes, which adds the necessary changes
# to support the pickle-ing of our defined data structures and ctype primitives.
#

'''
@author:       Pedram Amini
@license:      GNU General Public License 2.0 or later
@contact:      pedram.amini@gmail.com
@organization: www.openrce.org
'''

from my_ctypes import *
from windows_h import *

###
### manually declare entities from Tlhelp32.h since i was unable to import using h2xml.py.
###

TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPALL      = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)

class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize',             DWORD),
        ('cntUsage',           DWORD),
        ('th32ThreadID',       DWORD),
        ('th32OwnerProcessID', DWORD),
        ('tpBasePri',          DWORD),
        ('tpDeltaPri',         DWORD),
        ('dwFlags',            DWORD),
    ]

class PROCESSENTRY32(Structure):
    _fields_ = [
        ('dwSize',              DWORD),
        ('cntUsage',            DWORD),
        ('th32ProcessID',       DWORD),
        ('th32DefaultHeapID',   DWORD),
        ('th32ModuleID',        DWORD),
        ('cntThreads',          DWORD),
        ('th32ParentProcessID', DWORD),
        ('pcPriClassBase',      DWORD),
        ('dwFlags',             DWORD),
        ('szExeFile',           CHAR * 260),
]

class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize",        DWORD),
        ("th32ModuleID",  DWORD),
        ("th32ProcessID", DWORD),
        ("GlblcntUsage",  DWORD),
        ("ProccntUsage",  DWORD),
        ("modBaseAddr",   DWORD),
        ("modBaseSize",   DWORD),
        ("hModule",       DWORD),
        ("szModule",      CHAR * 256),
        ("szExePath",     CHAR * 260),
]

###
### manually declare various structures as needed.
###

class SYSDBG_MSR(Structure):
    _fields_ = [
        ("Address", c_ulong),
        ("Data",    c_ulonglong),
]

###
### manually declare various #define's as needed.
###

# debug event codes.
EXCEPTION_DEBUG_EVENT          = 0x00000001
CREATE_THREAD_DEBUG_EVENT      = 0x00000002
CREATE_PROCESS_DEBUG_EVENT     = 0x00000003
EXIT_THREAD_DEBUG_EVENT        = 0x00000004
EXIT_PROCESS_DEBUG_EVENT       = 0x00000005
LOAD_DLL_DEBUG_EVENT           = 0x00000006
UNLOAD_DLL_DEBUG_EVENT         = 0x00000007
OUTPUT_DEBUG_STRING_EVENT      = 0x00000008
RIP_EVENT                      = 0x00000009
USER_CALLBACK_DEBUG_EVENT      = 0xDEADBEEF     # added for callback support in debug event loop.

# debug exception codes.
EXCEPTION_ACCESS_VIOLATION     = 0xC0000005
EXCEPTION_BREAKPOINT           = 0x80000003
EXCEPTION_GUARD_PAGE           = 0x80000001
EXCEPTION_SINGLE_STEP          = 0x80000004

# hw breakpoint conditions
HW_ACCESS                      = 0x00000003
HW_EXECUTE                     = 0x00000000
HW_WRITE                       = 0x00000001

CONTEXT_CONTROL                = 0x00010001
CONTEXT_FULL                   = 0x00010007
CONTEXT_DEBUG_REGISTERS        = 0x00010010
CREATE_NEW_CONSOLE             = 0x00000010
DBG_CONTINUE                   = 0x00010002
DBG_EXCEPTION_NOT_HANDLED      = 0x80010001
DBG_EXCEPTION_HANDLED          = 0x00010001
DEBUG_PROCESS                  = 0x00000001
DEBUG_ONLY_THIS_PROCESS        = 0x00000002
EFLAGS_RF                      = 0x00010000
EFLAGS_TRAP                    = 0x00000100
ERROR_NO_MORE_FILES            = 0x00000012
FILE_MAP_READ                  = 0x00000004
FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM     = 0x00001000
INVALID_HANDLE_VALUE           = 0xFFFFFFFF
MEM_COMMIT                     = 0x00001000
MEM_DECOMMIT                   = 0x00004000
MEM_IMAGE                      = 0x01000000
MEM_RELEASE                    = 0x00008000
PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400
PROCESS_ALL_ACCESS             = 0x001F0FFF
SE_PRIVILEGE_ENABLED           = 0x00000002
SW_SHOW                        = 0x00000005
THREAD_ALL_ACCESS              = 0x001F03FF
TOKEN_ADJUST_PRIVILEGES        = 0x00000020

# for NtSystemDebugControl()
SysDbgReadMsr                  = 16
SysDbgWriteMsr                 = 17