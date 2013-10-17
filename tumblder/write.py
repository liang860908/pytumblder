#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import sys

import requests

import tumblder.exceptions
import tumblder.regex as regex

def print_log(prefix, msg, ret):
    r = '\r' if ret else ''
    e = '\n' if not ret else ''
    sys.stdout.write(r + prefix + msg + e)
    sys.stdout.flush()

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

    datas = None
    try:
        datas = session.get(url, stream=True).raw
        length = 100
        length_orig = length + 1
        to_read_sub = 8192
        try:
            length = int(datas.getheader('content-length'))
            length_orig = length
        except TypeError:
            to_read_sub = 0
            self.print_error('''No length given, download will
            go on but no percentage will be displayed.''')
        f = open(filepath, 'wb')
        while True:
            data = datas.read(to_read_sub, True)
            if data is b'':
                break
            length -= to_read_sub
            dl = str(int(100 - length * 100/ length_orig))
            print_log('downloading: ', '{0}% {1} ({2})'.format(dl, filename, url), True)
            f.write(data)
            f.flush()
            if length < 1:
                break
        f.close()
        print()
    except requests.exceptions.ConnectionError:
        raise tumblder.exceptions.DownloadPaused(url)

