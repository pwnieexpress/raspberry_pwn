#!/usr/bin/env python
import os
import sys
import bin.include


openfile=file("readme/CREDITS","r").readlines()


print '\n'
for line in openfile:
    print line.rstrip()
pause=raw_input("\b    Hit enter to return to main menu.")

