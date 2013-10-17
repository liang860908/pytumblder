#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import sys
import time

import requests

import tumblder.exceptions
import tumblder.download as download

from tumblder.common.logging import print_log
from tumblder import regex

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

    length_orig = length = 100
    to_read_sub = 8192 * 16

    stream, length = download.stream(url)
    length_orig = length

    f = open(filepath, 'wb')
    while length > 0:
        while True:
            try:
                datas, size = download.chunk(stream, to_read_sub)
                break
            except requests.exceptions.ConnectionError:
                print('download paused')
                time.sleep(2)
        if not size:
            break
        length -= size
        dl = int(100 - length * 100/ length_orig)
        dl = 100 if dl > 100 else dl
        print_log('downloading: ', '{0}% {1}'.format(dl, url), True)
        f.write(datas)
        f.flush()
    f.close()
    print()

