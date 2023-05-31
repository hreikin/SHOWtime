#!/usr/bin/env python

from showtime.context import Screen, ScreenContext
from showtime.ui import Header

import atexit
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p",
                    help="serial port to use as the output (default=/dev/ttyUSB0)",
                    type=str, default="/dev/ttyUSB0")
args = parser.parse_args()

ctx = ScreenContext(args.port, text_size=2, orientation=1, fg_colour=Screen.FG_WHITE, bg_colour=Screen.BG_BLUE)
header = Header()

while True:
    header.render(ctx, 0, "default title", 1)
