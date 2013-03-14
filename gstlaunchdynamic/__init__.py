#!/usr/bin/env python

import sys

from gi.repository import GLib
from gi.repository import Gst

from parser import Parser
from reader import setup_non_blocking_read

# init gstreamer, parse args
args = sys.argv[:]
Gst.init(args)

desc = ' '.join(args[1:])

# load gstreamer pipeline, press play

pipeline = Gst.parse_launch(desc)
pipeline.set_state(Gst.State.PLAYING)

# make stdin non-blocking
# when a line of input is recieved, parse it
# the parser has most of the logic

parser = Parser(pipeline)
setup_non_blocking_read(sys.stdin, parser.parse_line)

# run glib main loop

loop = GLib.MainLoop()
loop.run()

