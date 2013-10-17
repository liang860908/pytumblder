#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import sys

def print_log(prefix, msg, ret):
    r = '\r' if ret else ''
    e = '\n' if not ret else ''
    sys.stdout.write(r + prefix + msg + e)
    sys.stdout.flush()
