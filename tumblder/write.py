#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import sys
import time

import requests

import tumblder.exceptions
import tumblder.regex as regex
from tumblder.common.logging import print_log

def prepare(subdir):
    if not os.path.exists(subdir):
        os.makedirs(subdir)

def media(subdir, media, session):
    filename = media['name']
    filepath = subdir + '/' + filename
    url = media['url']

    fileexists = os.path.exists(filepath)

    if regex.STATICRES.match(url) and fileexists:
        raise tumblder.exceptions.StaticFileExists(filepath)
    elif fileexists:
        raise tumblder.exceptions.FileExists(filepath)

    length = 100
    length_orig = length + 1
    to_read_sub = 8192 * 16

    datas = session.get(url, stream=True).raw
    try:
        length = int(datas.getheader('content-length'))
        length_orig = length
    except TypeError:
        pass

    f = open(filepath, 'wb')
    while length > 0:
        while True:
            try:
                data = datas.read(to_read_sub, True)
                break
            except requests.exceptions.ConnectionError:
                print('download paused')
                time.sleep(2)
        if data is b'':
            break
        length -= to_read_sub
        dl = int(100 - length * 100/ length_orig)
        dl = 100 if dl > 100 else dl
        print_log('downloading: ', '{0}% {1} ({2})'.format(dl, filename, url), True)
        f.write(data)
        f.flush()
    f.close()
    print()

