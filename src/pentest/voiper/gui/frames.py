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

#Boa:Frame:MAINFRAME

import wx
import time
import threading

from fuzzer import fuzzers
from fuzzer.fuzzers import *

from protocol_logic.sip_utilities import SIPRegistrar

def create(parent):
    return MainFrame(parent)

[wxID_MAINFRAME, wxID_MAINFRAMECRASHDETECTIONSTATICBOX, 
 wxID_MAINFRAMECTRLPANELSTATICBOX, wxID_MAINFRAMEDETECTEDCRASHESSTATICTXT, 
 wxID_MAINFRAMEFUZZERCOMBOBOX, wxID_MAINFRAMEFUZZERCONFIGURATIONSTATICBOX, 
 wxID_MAINFRAMEFUZZERSTATICTEXT, wxID_MAINFRAMELEVELCOMBOBOX, 
 wxID_MAINFRAMELEVELSTATICTXT, wxID_MAINFRAMELOGSTATICBOX, wxID_MAINFRAMELOGTXTCTRL, 
 wxID_MAINFRAMEOPTIONALSTATICBOX, wxID_MAINFRAMEPAUSEBUTTON, 
 wxID_MAINFRAMEPEDRPCPORTTXTCTRL, wxID_MAINFRAMEPEDRPCSTATICTXT, 
 wxID_MAINFRAMEPROGRESSGUAGE, wxID_MAINFRAMERESTARTINTERVALSTATICTEXT, 
 wxID_MAINFRAMERESTARTINTERVALTXTCTRL, wxID_MAINFRAMESESSIONNAMESTATICTXT, 
 wxID_MAINFRAMESESSIONNAMETXTCTRL, wxID_MAINFRAMESKIPSTATICTEXT, 
 wxID_MAINFRAMESKIPTXTCTRL, wxID_MAINFRAMESTARTBUTTON, wxID_MAINFRAMESTARTCMDTXTCTRL, 
 wxID_MAINFRAMESTATICLINE1, wxID_MAINFRAMESTATICTEXT1, wxID_MAINFRAMESTOPCMDSTATICTXT, 
 wxID_MAINFRAMESTOPCMDTXTCTRL, wxID_MAINFRAMETARGETHOSTSTATICTEXT, 
 wxID_MAINFRAMETARGETHOSTTXTCTRL, wxID_MAINFRAMETARGETPORTSTATICTEXT, 
 wxID_MAINFRAMETARGETPORTTXTCTRL, wxID_MAINFRAMETARGETSELECTIONSTATICBOX, 
 wxID_MAINFRAMETESTSSENTTXTCTRL, wxID_MAINFRAMEWFRCHECKBOX, 
 wxID_MAINFRAMEWFRSTATICTEXT, wxID_MAINFRAMEMAXSTRINGTXTCTRL, wxID_MAINFRAMEMAXSTRINGSTATICTEXT,
] = [wx.NewId() for _init_ctrls in range(38)]

VERSION = "v0.07"

class MainFrame(wx.Frame):

    def _init_sizers(self):
        # generated method, don't edit
        self.mainGridSizer = wx.GridSizer(cols=2, hgap=10, rows=2, vgap=10)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='', parent=prnt,
              pos=wx.Point(403, 115), size=wx.Size(561, 741),
              style=wx.DEFAULT_FRAME_STYLE,
              title='VoIPER : VoIP Exploit Research tookit ' + VERSION )
        self.SetClientSize(wx.Size(553, 707))
        self.SetBackgroundColour(wx.Colour(230, 230, 230))

        self.targetHostTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMETARGETHOSTTXTCTRL,
              name='targetHostTxtCtrl', parent=self, pos=wx.Point(96, 32),
              size=wx.Size(100, 21), style=wx.TE_RIGHT, value='127.0.0.1')

        self.targetHostStaticText = wx.StaticText(id=wxID_MAINFRAMETARGETHOSTSTATICTEXT,
              label='Target host', name='targetHostStaticText', parent=self,
              pos=wx.Point(24, 32), size=wx.Size(56, 13), style=0)
        self.targetHostStaticText.SetToolTipString('Target host')

        self.targetPortStaticText = wx.StaticText(id=wxID_MAINFRAMETARGETPORTSTATICTEXT,
              label='Target port', name='targetPortStaticText', parent=self,
              pos=wx.Point(24, 72), size=wx.Size(55, 13), style=0)

        self.targetPortTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMETARGETPORTTXTCTRL,
              name='targetPortTxtCtrl', parent=self, pos=wx.Point(96, 72),
              size=wx.Size(100, 21), style=wx.TE_RIGHT, value='5060')

        self.targetSelectionStaticBox = wx.StaticBox(id=wxID_MAINFRAMETARGETSELECTIONSTATICBOX,
              label='Target Selection', name='targetSelectionStaticBox',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(208, 96), style=0)

        self.fuzzerConfigurationStaticBox = wx.StaticBox(id=wxID_MAINFRAMEFUZZERCONFIGURATIONSTATICBOX,
              label='Fuzzer Configuration', name='fuzzerConfigurationStaticBox',
              parent=self, pos=wx.Point(296, 8), size=wx.Size(248, 96),
              style=0)

        self.fuzzerComboBox = wx.ComboBox(choices=self.fuzzer_list,
              id=wxID_MAINFRAMEFUZZERCOMBOBOX, name='fuzzerComboBox', parent=self,
              pos=wx.Point(400, 32), size=wx.Size(130, 21),
              style=wx.CB_READONLY, value='Select a fuzzer')
        self.fuzzerComboBox.SetLabel('')
        self.fuzzerComboBox.Bind(wx.EVT_COMBOBOX, self.OnFuzzerComboBoxCombobox,
              id=wxID_MAINFRAMEFUZZERCOMBOBOX)        

        self.fuzzerStaticText = wx.StaticText(id=wxID_MAINFRAMEFUZZERSTATICTEXT,
              label='Fuzzer', name='fuzzerStaticText', parent=self,
              pos=wx.Point(312, 32), size=wx.Size(32, 13), style=0)

        self.sessionNameStaticTxt = wx.StaticText(id=wxID_MAINFRAMESESSIONNAMESTATICTXT,
              label='Session Name', name='sessionNameStaticTxt', parent=self,
              pos=wx.Point(312, 72), size=wx.Size(66, 13), style=0)

        self.sessionNameTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMESESSIONNAMETXTCTRL,
              name='sessionNameTxtCtrl', parent=self, pos=wx.Point(400, 72),
              size=wx.Size(128, 21), style=0,
              value='Audit folder in sessions/')

        self.crashDetectionStaticBox = wx.StaticBox(id=wxID_MAINFRAMECRASHDETECTIONSTATICBOX,
              label='Crash Detection/Target Management',
              name='crashDetectionStaticBox', parent=self, pos=wx.Point(8, 128),
              size=wx.Size(208, 184), style=0)

        self.levelStaticTxt = wx.StaticText(id=wxID_MAINFRAMELEVELSTATICTXT,
              label='Level', name='levelStaticTxt', parent=self,
              pos=wx.Point(24, 152), size=wx.Size(25, 13), style=0)

        self.levelComboBox = wx.ComboBox(choices=['0', '1', '2', '3'],
              id=wxID_MAINFRAMELEVELCOMBOBOX, name='levelComboBox', parent=self,
              pos=wx.Point(144, 152), size=wx.Size(50, 21),
              style=wx.CB_READONLY, value='0')
        self.levelComboBox.SetLabel('0')
        self.levelComboBox.Bind(wx.EVT_COMBOBOX, self.OnLevelComboBoxCombobox,
              id=wxID_MAINFRAMELEVELCOMBOBOX)

        self.pedRPCStaticTxt = wx.StaticText(id=wxID_MAINFRAMEPEDRPCSTATICTXT,
              label='PedRPC port', name='pedRPCStaticTxt', parent=self,
              pos=wx.Point(24, 184), size=wx.Size(61, 13), style=0)

        self.pedRpcPortTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMEPEDRPCPORTTXTCTRL,
              name='pedRpcPortTxtCtrl', parent=self, pos=wx.Point(144, 184),
              size=wx.Size(52, 21), style=wx.TE_RIGHT, value='26002')
        self.pedRpcPortTxtCtrl.Enable(False)

        self.staticText1 = wx.StaticText(id=wxID_MAINFRAMESTATICTEXT1,
              label='Start Cmd', name='staticText1', parent=self,
              pos=wx.Point(24, 248), size=wx.Size(48, 13), style=0)

        self.startCmdTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMESTARTCMDTXTCTRL,
              name='startCmdTxtCtrl', parent=self, pos=wx.Point(96, 248),
              size=wx.Size(100, 21), style=0, value='Target start cmd')
        self.startCmdTxtCtrl.Enable(False)

        self.stopCmdStaticTxt = wx.StaticText(id=wxID_MAINFRAMESTOPCMDSTATICTXT,
              label='Stop Cmd', name='stopCmdStaticTxt', parent=self,
              pos=wx.Point(24, 280), size=wx.Size(46, 13), style=0)

        self.stopCmdTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMESTOPCMDTXTCTRL,
              name='stopCmdTxtCtrl', parent=self, pos=wx.Point(96, 280),
              size=wx.Size(100, 21), style=0, value='TERMINATE_PID')
        self.stopCmdTxtCtrl.Enable(False)

        self.optionalStaticBox = wx.StaticBox(id=wxID_MAINFRAMEOPTIONALSTATICBOX,
              label='Optional', name='optionalStaticBox', parent=self,
              pos=wx.Point(296, 128), size=wx.Size(248, 120), style=0)

        self.wfrCheckBox = wx.CheckBox(id=wxID_MAINFRAMEWFRCHECKBOX, label='',
              name='wfrCheckBox', parent=self, pos=wx.Point(512, 152),
              size=wx.Size(16, 13), style=0)
        self.wfrCheckBox.SetValue(False)

        self.wfrStaticText = wx.StaticText(id=wxID_MAINFRAMEWFRSTATICTEXT,
              label='Wait for client registration', name='wfrStaticText',
              parent=self, pos=wx.Point(312, 152), size=wx.Size(125, 13),
              style=0)

        self.skipStaticText = wx.StaticText(id=wxID_MAINFRAMESKIPSTATICTEXT,
              label='Tests to skip', name='skipStaticText', parent=self,
              pos=wx.Point(312, 184), size=wx.Size(60, 13), style=0)

        self.skipTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMESKIPTXTCTRL,
              name='skipTxtCtrl', parent=self, pos=wx.Point(474, 184),
              size=wx.Size(50, 21), style=wx.TE_RIGHT, value='0')

        self.maxStringStaticText = wx.StaticText(id=wxID_MAINFRAMEMAXSTRINGSTATICTEXT,
              label='Max fuzz data', name='maxStringStaticText', parent=self,
              pos=wx.Point(312, 216), size=wx.Size(86, 13), style=0)

        self.maxStringTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMEMAXSTRINGTXTCTRL,
              name='maxStringTxtCtrl', parent=self, pos=wx.Point(474, 216),
              size=wx.Size(50, 21), style=wx.TE_RIGHT, value='8192')

        self.staticLine1 = wx.StaticLine(id=wxID_MAINFRAMESTATICLINE1,
              name='staticLine1', parent=self, pos=wx.Point(48, 338),
              size=wx.Size(464, 2), style=0)

        self.logStaticBox = wx.StaticBox(id=wxID_MAINFRAMELOGSTATICBOX,
              label='Log', name='logStaticBox', parent=self, pos=wx.Point(8,
              360), size=wx.Size(536, 336), style=0)

        self.logTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMELOGTXTCTRL,
              name='logTxtCtrl', parent=self, pos=wx.Point(16, 448),
              size=wx.Size(520, 232),
              style=wx.VSCROLL | wx.TE_MULTILINE | wx.TE_LINEWRAP | wx.TE_READONLY,
              value='VoIPER - VoIP Exploit Research toolkit ' + VERSION + ' by nnp\nhttp://voiper.sourceforge.net\n\n')
        self.logTxtCtrl.SetMaxLength(0)
        self.logTxtCtrl.Bind(wx.EVT_TEXT_MAXLEN, self.OnLogTxtCtrlTextMaxlen,
              id=wxID_MAINFRAMELOGTXTCTRL)

        self.ctrlPanelStaticBox = wx.StaticBox(id=wxID_MAINFRAMECTRLPANELSTATICBOX,
              label='Control Panel', name='ctrlPanelStaticBox', parent=self,
              pos=wx.Point(296, 262), size=wx.Size(248, 48), style=0)

        self.startButton = wx.Button(id=wxID_MAINFRAMESTARTBUTTON, label='Start',
              name='startButton', parent=self, pos=wx.Point(312, 280),
              size=wx.Size(75, 23), style=0)
        self.startButton.Bind(wx.EVT_BUTTON, self.OnStartButtonButton,
              id=wxID_MAINFRAMESTARTBUTTON)

        self.pauseButton = wx.Button(id=wxID_MAINFRAMEPAUSEBUTTON, label='Pause',
              name='pauseButton', parent=self, pos=wx.Point(456, 280),
              size=wx.Size(75, 23), style=0)
        self.pauseButton.Bind(wx.EVT_BUTTON, self.OnPauseButtonButton,
              id=wxID_MAINFRAMEPAUSEBUTTON)

        self.progressGuage = wx.Gauge(id=wxID_MAINFRAMEPROGRESSGUAGE,
              name='progressGuage', parent=self, pos=wx.Point(16, 408),
              range=1000, size=wx.Size(520, 28), style=wx.GA_HORIZONTAL)

        self.testsSentTxtCtrl = wx.StaticText(id=wxID_MAINFRAMETESTSSENTTXTCTRL,
              label=' Sent 0/0 test cases', name='testsSentTxtCtrl',
              parent=self, pos=wx.Point(16, 384), size=wx.Size(96, 13),
              style=0)

        self.restartIntervalStaticText = wx.StaticText(id=wxID_MAINFRAMERESTARTINTERVALSTATICTEXT,
              label='Restart Interval', name='restartIntervalStaticText',
              parent=self, pos=wx.Point(24, 216), size=wx.Size(77, 13),
              style=0)

        self.restartIntervalTxtCtrl = wx.TextCtrl(id=wxID_MAINFRAMERESTARTINTERVALTXTCTRL,
              name='restartIntervalTxtCtrl', parent=self, pos=wx.Point(136,
              216), size=wx.Size(60, 21), style=wx.TE_RIGHT, value='None')
        self.restartIntervalTxtCtrl.Enable(False)

        self.detectedCrashesStaticTxt = wx.StaticText(id=wxID_MAINFRAMEDETECTEDCRASHESSTATICTXT,
              label='0 detected crashes', name='detectedCrashesStaticTxt',
              parent=self, pos=wx.Point(440, 384), size=wx.Size(92, 13),
              style=0)

        self._init_sizers()

    def get_fuzzers(self):
        for object in dir(fuzzers):
            if object.find('Fuzzer') != -1 and object.find('Abstract') == -1:
                self.fuzzer_list.append(object)
        
    def __init__(self, parent):
        self.fuzzer_list = ['Select a fuzzer']
        self.verbosity = 2
        self.started = False
        self.paused = False
        self.get_fuzzers()        
        self._init_ctrls(parent)                

    def gatherOptions(self):
        self.fuzzer = self.fuzzerComboBox.GetValue()
        self.targetHost = self.targetHostTxtCtrl.GetValue()
        self.targetPort = self.targetPortTxtCtrl.GetValue()
        self.sessionName = self.sessionNameTxtCtrl.GetValue()
        self.crashDetectionLevel = self.levelComboBox.GetValue()
        self.pedRpcRemotePort = self.pedRpcPortTxtCtrl.GetValue()
        self.startCmd = self.startCmdTxtCtrl.GetValue()
        self.stopCmd = self.stopCmdTxtCtrl.GetValue()        
        self.wfr = self.wfrCheckBox.GetValue()
        self.skipTestNum = self.skipTxtCtrl.GetValue()
        self.restartInterval = self.restartIntervalTxtCtrl.GetValue()
        self.maxStringLen = self.maxStringTxtCtrl.GetValue()

    def checkOptions(self):
        if self.fuzzer == 'Select a fuzzer':
            return 'Select a fuzzer'        
        if len(self.targetHost) == 0:
            return 'Please enter a target host'
        if len(self.targetPort) == 0:
            return 'Please enter a target port'
        try:
            self.targetPort = int(self.targetPort)
        except:
            return 'Positive integer required for target port'

        if len(self.sessionName) == 0 or self.sessionName == "Audit folder in sessions/":
            return 'Please enter a session name'
        else:
            self.sessionName = '/'.join(["sessions", self.sessionName])
            
        if self.restartInterval == 'None' or self.restartInterval == '0': 
            self.restartInterval = 0
        else:
            try:
                self.restartInterval= int(self.restartInterval)            
                if self.restartInterval < 0:
                    return 'Positive integer required for restart interval'   
            except:
                return 'Positive integer required for restart interval'
            
        self.crashDetectionLevel = int(self.crashDetectionLevel)
        if self.crashDetectionLevel == 3:            
            if len(self.pedRpcRemotePort) == 0:
                return 'PedRPC port required for crash detection/target management level 3(Default=26002)'
            try:
                self.pedRpcRemotePort = int(self.pedRpcRemotePort)
            except:
                return 'Positive integer required for PEDRPC port'                
                        
                if len(self.startCmd) == 0:
                    return 'Start command required for crash detection/target management level 3 with restart interval'
                if len(self.stopCmd) == 0:
                    return 'Stop command required for crash detection/target management level 3(Default=TERMINATE_PID with restart interval'
                
        try:
            self.skipTestNum = int(self.skipTestNum)            
            if self.skipTestNum < 0:
                return 'Positive integer required for number of tests to skip'   
        except:
            return 'Positive integer required for number of tests to skip'

        try:
            self.maxStringLen = int(self.maxStringLen)            
            if self.skipTestNum < 0:
                return 'Positive integer required for max fuzz string length'   
        except:
            return 'Positive integer required for max fuzz string length'
        

        return self.checkSessionDir()

    def waitForRegister(self):
        sr = SIPRegistrar('0.0.0.0', 5060)
        sr.log = self.updateLog
        self.updateLog('[+] Waiting for register request')
        sr.waitForRegister()

    def checkSessionDir(self):
        if not os.path.exists(self.sessionName):
            self.updateLog('[!] Path %s does not exist or we do not have sufficient permissions.' % self.sessionName)
            self.updateLog('[+] Attempting to create %s' % self.sessionName)
            os.mkdir(self.sessionName)
            if not os.path.exists(self.sessionName):
                self.updateLog('[!] Could not create directory %s. Please provide a different path')
                return 'Error creating or using the provided session directory. See log for details'
            else:
                self.updateLog('[+] Successfully created %s' % self.sessionName)

            return None
        
    def OnStartButtonButton(self, event): 
        # gather options and perform checks   
        if self.started == False:            
            self.gatherOptions()
            errMsg = self.checkOptions()
            if errMsg:
                wx.MessageDialog(self, errMsg, caption="Error", style=wx.OK).ShowModal()                
            else:
                self.logTxtCtrl.AppendText('-=-'*30 + '\n')
                self.fuzzer_obj = eval(self.fuzzer + '(self.sessionName, "udp", self.targetHost,\
                    self.targetPort, int(self.crashDetectionLevel), self.skipTestNum, \
                    self.startCmd, self.stopCmd, self.pedRpcRemotePort, self.restartInterval, \
                    self.updateLog, max_len=self.maxStringLen)')

                # Some code to make the 'low coupling, high cohesion' people cry
                self.fuzzer_obj.sess.running_flag = True
                if self.crashDetectionLevel == 3:
                    self.fuzzer_obj.target.running_flag = True
                    self.fuzzer_obj.target.procmon.running_flag = True
                self.fuzzer_obj.using_GUI = True
                self.fuzzer_obj.pause_GUI = self.OnPauseButtonButtonNoEvent
                # override some methods in the fuzzer with our methods
                self.fuzzer_obj.sess.updateProgressBar = self.updateProgressBar
                self.fuzzer_obj.sess.update_GUI_crashes = self.updateDetectedCrashes

                if self.wfr:
                    self.fuzzer_obj.sess.waitForRegister = self.waitForRegister
                    self.waitForRegister()
                
                self.startButton.Label = "Stop"
                self.fuzzer_thread = threading.Thread(target=self.fuzzer_obj.fuzz)
                self.fuzzer_thread.start()

                self.paused = False
                self.pauseButton.Label = "Pause"
                self.fuzzer_obj.sess.pause_flag = False
                
                self.started = True
        else:
            # we are a stop button now so stop the fuzzer
            self.fuzzer_obj.sess.running_flag = False
            if self.crashDetectionLevel == 3:
                self.fuzzer_obj.target.running_flag = False
                self.fuzzer_obj.target.procmon.running_flag = False
            if self.fuzzer_obj.__dict__.has_key('invite_canceler'):
                self.fuzzer_obj.invite_canceler.kill_cancel_threads()
            self.started = False
            #self.fuzzer.stop()
            self.startButton.Label = "Start"
            
    def OnLevelComboBoxCombobox(self, event):
        if self.levelComboBox.GetValue() == '3':
            self.pedRpcPortTxtCtrl.Enabled = True
            self.startCmdTxtCtrl.Enabled = True
            self.stopCmdTxtCtrl.Enabled = True
            self.restartIntervalTxtCtrl.Enabled = True
        else:
            self.pedRpcPortTxtCtrl.Enabled = False
            self.startCmdTxtCtrl.Enabled = False
            self.stopCmdTxtCtrl.Enabled = False
            self.restartIntervalTxtCtrl.Enabled = False

    def OnFuzzerComboBoxCombobox(self, event):
        fuzzer = self.fuzzerComboBox.GetValue()
        h = eval(fuzzer + ".info()")
        self.updateLog(h + '\n', showTime=False)

    def OnLogTxtCtrlTextMaxlen(self, event):
        # if the log window is full (apparently about 32k characters)
        # dump to a file and clear
        
        log_name = time.ctime().replace(" ", "") + ".log"
        outputFile = open(log_name, 'w')
        outputFile.write(self.logTxtCtrl.GetValue())
        outputFile.close()
        self.logTxtCtrl.Clear()
        self.updateLog("[!] Log max length reached. Dumped to " + log_name)

    def updateLog(self, text, level=1, showTime=True):
        if level <= self.verbosity:
            if showTime:
                self.logTxtCtrl.AppendText("[%s] %s\n" % (time.strftime("%H:%M.%S"),text))
            else:
                self.logTxtCtrl.AppendText(text)

    def updateProgressBar(self, x, y):
        '''
        @type x: Integer
        @param x: Number of fuzz cases sent so far
        @type y: Integer
        @param y: Total number of fuzz cases
        '''
        
        self.testsSentTxtCtrl.SetLabel(" Sent %d/%d test cases" % (x, y))
        val = float(x)/float(y) * 1000
        self.progressGuage.SetValue(val)
        
    def updateDetectedCrashes(self, crashes):        
        if crashes == 1:
            label = "1 detected crash"
        else:
            label = "%d detected crashes" % crashes
            
        self.detectedCrashesStaticTxt.SetLabel(label)

    def OnPauseButtonButtonNoEvent(self):
        self.OnPauseButtonButton(None)
        
    def OnPauseButtonButton(self, event): 
        if self.started and self.paused == False:               
            self.paused = True
            self.pauseButton.Label = "Restart"
            self.fuzzer_obj.sess.pause_flag = True
        elif self.started:
            self.paused = False
            self.pauseButton.Label = "Pause"
            self.fuzzer_obj.sess.pause_flag = False

        
