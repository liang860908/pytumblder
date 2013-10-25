#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import shutil
import tempfile

import tumblder.exceptions
import tumblder.download as download

from tumblder.pycommon.logging import print_log
from tumblder import regex

STOPWRITE = False

def prepare(subdir):
    if not os.path.exists(subdir):
        os.makedirs(subdir)

def media(subdir, media):
    filename = media[0]['name']
    filepath = subdir + '/' + filename
    url = media[0]['url']

    fileexists = os.path.exists(filepath)

    if regex.STATICRES.match(url) and fileexists:
        raise tumblder.exceptions.StaticFileExists(filepath)
    elif fileexists:
        raise tumblder.exceptions.FileExists(filepath)

    length_orig = length = 100
    to_read_sub = 8192 * 16

    stream, length = download.streaming(url)
    length_orig = length

    tmpfile = tempfile.NamedTemporaryFile(prefix='pytumblder_', delete=False)
    while length > 0 and not STOPWRITE:
        datas, size = download.chunk(stream, to_read_sub)
        if not size:
            break
        length -= size
        dl = int(100 - length * 100/ length_orig)
        dl = 100 if dl > 100 else dl
        print_log('downloading: ', 'page {2} {1} - {0}%'.format(dl, url, media[1]), True)
        tmpfile.write(datas)
        tmpfile.flush()
    tmpfile.close()

    if STOPWRITE:
        os.remove(tmpfile.name)
    else:
        shutil.move(tmpfile.name, filepath)

