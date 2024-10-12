#!/usr/bin/env python

import sys
import gi

gi.require_version('Gst', '1.0')

from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GObject

from gstlaunchdynamic.parser import Parser
from gstlaunchdynamic.reader import setup_non_blocking_read

def show_pipeline(pipeline):

   print("\nPrint all elements of the pipeline\n")

   iter = Gst.Bin.iterate_elements(pipeline)

   while True:
       res = Gst.Iterator.next(iter)
       if res[1]:
           name = res[1].name
           print(f"\t- {name}")
       if res[0] == Gst.IteratorResult.DONE:
           break

# init gstreamer, parse args
args = sys.argv[:]
Gst.init(args)

desc = ' '.join(args[1:])
print ("pipeline: "+desc)

# load gstreamer pipeline, press play

pipeline = Gst.parse_launch(desc)
pipeline.set_state(Gst.State.PLAYING)
show_pipeline(pipeline)

# make stdin non-blocking
# when a line of input is recieved, parse it
# the parser has most of the logic

parser = Parser(pipeline)
setup_non_blocking_read(sys.stdin, parser.parse_line)

# run glib main loop

loop = GLib.MainLoop()
loop.run()

