import ast
import re

from gi.repository import Gst

# for the moment...
gst_eval = ast.literal_eval

class Parser(object):

    def process_pipeline(self, description, autoplay):
        if description:
            # load gstreamer pipeline, press play
            parsed = Gst.parse_launch(description)
            if type(parsed) == Gst.Pipeline:
                self.pipeline = parsed
            else:
                self.pipeline = Gst.Pipeline.new()
                self.pipeline.add(parsed)
        if autoplay:
            self.pipeline.set_state(Gst.State.PLAYING)
        self.show_pipeline()

    def __init__(self, description):
        self.process_pipeline(description, True)

        self.expressions = [
            (r'^\s*(\w+)\.([\w-]+)\s*=\s*(.+)\s*$', self.set_property),
            (r'^\s*(\w+)(?:\.(\w+))?\s*([-x])>\s*(\w+)(?:\.(\w+))?\s*$', self.link_pads),
            (r'^\s*\+\s*(\w+)(?: (.*))?\s*$', self.add_element),
            (r'^\s*-\s*(\w+)\s*$', self.remove_element),
            (r'^\s*(stop|play|pause)\s*$', self.set_state),
            (r'^\s*help\s*$', self.help),
            (r'^\s*pipeline\s*$', self.show_pipeline),
        ]

        self.expressions = [
            (re.compile(regex), fn)
            for regex, fn in self.expressions
        ]

    def show_pipeline(self):

        print(f"elements of pipeline: {self.pipeline.name}")

        iter = Gst.Bin.iterate_elements(self.pipeline)
        while True:
            res = Gst.Iterator.next(iter)
            if res[1]:
                name = res[1].name
                print(f"\t- {name}")
                for pad in res[1].pads:
                    try:
                        padtype = 'UNKNOWN'
                        if pad.direction == Gst.PadDirection.SRC:
                            padtype = 'SOURCE'
                        elif pad.direction == Gst.PadDirection.SINK:
                            padtype = 'SINK'
                        print(f"\t- pad name: {pad.name}, type: {padtype}")
                    except:
                        pass
            if res[0] == Gst.IteratorResult.DONE:
                break

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
            try:
                self.process_pipeline(line, False)
            except Exception as e:
                print(f"Error: could not parse line: {e=}, {type(e)=}")

    def set_property(self, target, attr, value):
        el = self.pipeline.get_by_name(target)
        value = gst_eval(value)
        el.set_property(attr, value)

    def link_pads(self, src, src_pad, char, dst, dst_pad):
        src_el = self.pipeline.get_by_name(src)
        dst_el = self.pipeline.get_by_name(dst)

        if char == '-':
            success = src_el.link_pads(src_pad, dst_el, dst_pad)
            if not success:
                success = dst_el.link_pads(dst_pad, src_el, src_pad)
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
        #TODO:Sometimes it needs pause and play to show the window
        self.pipeline.set_state(state)

    def help(self):
        print("""\
                Help:
                Commands:
                Edit property:
                nodename.property = value
                Link pads:
                Join:
                nodename -> nodename2
                Unlink:
                nodename x> nodename2
                Add element:
                +nodename config
                -nodename config
                Control:
                stop
                play
                pause
                Help:
                help
                Render:
                render
        """)

    def add_element(self, kind, properties):
        # TODO: write a proper parser, and don't have this here
        try:
            name = None
            props = None
            if properties:
                props = dict(
                    pair.split('=', 1)
                    for pair in properties.split(' ')
                )

                # create the element
                name = props.pop('name', None)

            element = Gst.ElementFactory.make(kind, name)
            if not element:
                raise Exception(f"Cannot parse description '{kind}'")

            # set the properties
            if props:
                for key, value in props:
                    value = gst_eval(value)
                    element.set_property(key, value)

            self.pipeline.add(element)
            self.show_pipeline()
        except Exception as e:
            print(f"Error adding element: {e}")

    def remove_element(self, name):
        try:
            element = self.pipeline.get_by_name(name)
            if not element:
                raise Exception(f"Cannot find element by name '{name}'")
            self.pipeline.remove(element)
        except Exception as e:
            print(f"Error removing element: {e}")
