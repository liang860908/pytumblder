#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os

import tumblder.exceptions
import tumblder.regex as regex

def prepare(subdir):
    if not os.path.exists(subdir):
        os.makedirs(subdir)

def media(subdir, media):
    filename = media['name']
    filepath = subdir + '/' + filename
    turl = media['url']
    msgurl = ' (' + turl + ')'

    fileexists = os.path.exists(filepath)

    if regex.STATICRES.match(turl) and fileexists:
        raise tumblder.exceptions.StaticFileExists(filepath)
    elif fileexists:
        raise tumblder.exceptions.FileExists(filepath)

    datas = None
    while True:
        try:
            print('downloading: ' + filename + msgurl)
            datas = session.get(turl).content
            break
        except requests.exceptions.ConnectionError:
            raise tumblder.exceptions.DownloadPaused(turl)

    f = open(filepath, 'wb')
    f.write(datas)
    f.close()
