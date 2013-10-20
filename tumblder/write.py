#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import sys
import time
import shutil
import tempfile

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

    tmpfile = tempfile.NamedTemporaryFile(prefix='pytumblder_', delete=False)
    while length > 0:
        datas, size = download.chunk(stream, to_read_sub)
        if not size:
            break
        length -= size
        dl = int(100 - length * 100/ length_orig)
        dl = 100 if dl > 100 else dl
        print_log('downloading: ', '{0}% {1}'.format(dl, url), True)
        tmpfile.write(datas)
        tmpfile.flush()
    tmpfile.close()
    shutil.move(tmpfile.name, filepath)
    print('')

