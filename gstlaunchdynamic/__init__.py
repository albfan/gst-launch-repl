#!/usr/bin/env python

import sys
import gi

gi.require_version('Gst', '1.0')

from gi.repository import GLib
from gi.repository import Gst

from gstlaunchdynamic.parser import Parser
from gstlaunchdynamic.reader import setup_non_blocking_read

# init gstreamer, parse args
args = sys.argv[:]
Gst.init(args)

desc = ' '.join(args[1:])

# make stdin non-blocking
# when a line of input is recieved, parse it
# the parser has most of the logic

parser = Parser(desc)
setup_non_blocking_read(sys.stdin, parser.parse_line)

# run glib main loop

loop = GLib.MainLoop()
loop.run()

