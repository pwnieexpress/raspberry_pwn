#!/usr/bin/env python
#Boa:App:BoaApp

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

import wx

from gui import frames

modules ={u'gui/MainFrame': [1, 'Main frame of Application', 'gui/frames.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = frames.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
