#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import time
import sys

import tumblder

def stream(url):
    stream = tumblder.session.get(url, stream=True).raw
    try:
        length = int(stream.getheader('content-length'))
    except TypeError:
        length = -1
    return stream, length

def chunk(stream, chunksize):
    datas = stream.read(chunksize, True)
    size = len(datas)
    return datas, size

def all(stream):
    data = b''
    while True:
        data += getchunk(stream, 8192)
        if data is b'':
            break
    return data
