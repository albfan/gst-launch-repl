import fcntl
import os

from gi.repository import GLib

def setup_non_blocking_read(f, on_line):
    fd = f.fileno()

    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    buf = ['']
    def on_data_available(fd, condition):
        data = f.read()
        buf[0] += data

        lines = buf[0].split('\n')
        buf[0] = lines.pop()

        for line in lines:
            on_line(line)

        return True

    GLib.io_add_watch(
        fd,
        GLib.IOCondition.IN,
        on_data_available,
    )

