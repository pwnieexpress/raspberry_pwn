#!/usr/bin/env python

import sys;
import binascii;

from GoodFETSmartCard import GoodFETSmartCard;
from intelhex import IntelHex16bit, IntelHex;

#Initialize FET and set baud rate
client=GoodFETSmartCard();
client.serInit()

#Connect to target
client.start();
