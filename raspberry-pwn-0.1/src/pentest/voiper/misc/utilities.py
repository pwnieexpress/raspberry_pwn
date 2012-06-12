'''
This file is part of VoIPER.

VoIPER is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

VoIPER is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VoIPER.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2008, http://www.unprotectedhex.com
Contact: nnp@unprotectedhex.com
'''

import time

class Logger:
    def __init__(self, verbosity=2):
        self.verbosity = verbosity

    def log(self, text, level=1):
        '''
        Default log function. Prints text to stdout. Override for different logging methods.
        '''
        
        if level <= self.verbosity:
            print "[%s] %s" % (time.strftime("%H:%M.%S"),text)
