#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:02:08 2020

@author: wukeying
"""

import time
import serial

def foo():
    ardu= serial.Serial('COM9',9600, timeout=.1)
    time.sleep(1)
    ardu.write(match(refs, hist)）
    time.sleep(1)
    #ardu.close()
while(1)
foo()
