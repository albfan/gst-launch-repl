import ast
import re

from gi.repository import Gst

# for the moment...
gst_eval = ast.literal_eval

class Parser(object):
    def __init__(self, pipeline):
        self.pipeline = pipeline

        self.expressions = [
            ('^(\w+)\.(\w+) = (.+)$', self.set_property),
            ('^(\w+)(?:\.(\w+))? ([-x])> (\w+)(?:\.(\w+))?$', self.link_pads),
            ('^\+ (\w+)(?: (.*))?$', self.add_element),
            ('^- (\w+)$', self.remove_element),
            ('^(stop|play|pause)$', self.set_state),
        ]

        self.expressions = [
            (re.compile(regex), fn)
            for regex, fn in self.expressions
        ]

    def parse_line(self, line):
        for regex, fn in self.expressions:
            m = regex.match(line)
            if m:
                try:
                    fn(*m.groups())
                except Exception:
                    import traceback
                    traceback.print_exc()
                break
        else:
            print ('Error: could not parse line.')

    def set_property(self, target, attr, value):
        el = self.pipeline.get_by_name(target)
        value = gst_eval(value)
        el.set_property(attr, value)

    def link_pads(self, src, src_pad, char, dst, dst_pad):
        src_el = self.pipeline.get_by_name(src)
        dst_el = self.pipeline.get_by_name(dst)

        print (src_el, src_pad, char, dst_el, dst_pad)

        if char == '-':
            success = src_el.link_pads(src_pad, dst_el, dst_pad)
            if not success:
                print ('Could not link pads.')

        elif char == 'x':
            success = src_el.unlink_pads(src_pad, dst_el, dst_pad)
            if not success:
                print ('Could not unlink pads.')

    def set_state(self, state):
        state = {
            'stop': Gst.State.READY,
            'play': Gst.State.PLAYING,
            'pause': Gst.State.PAUSED,
        }[state]
        self.pipeline.set_state(state)

    def add_element(self, kind, properties):
        # TODO: write a proper parser, and don't have this here
        properties = dict(
            pair.split('=', 1)
            for pair in properties.split(' ')
        )

        # create the element
        name = properties.pop('name', None)
        element = Gst.ElementFactory.make(kind, name)

        # set the properties
        for key, value in properties:
            value = gst_eval(value)
            element.set_property(key, value)

        self.pipeline.add(element)

    def remove_element(self, name):
        element = self.pipeline.get_by_name(name)
        self.pipeline.remove(element)
