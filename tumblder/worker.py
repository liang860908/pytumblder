#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import time
import sys

from importlib import import_module

import requests

import tumblder.write
import tumblder.exceptions
import tumblder.regex as regex

from tumblder.common.logging import print_log

session = requests.Session()

STAT_new_medias = 0

def pagemedias(args, page, getter):
    medias = []

    content = getter.content(args.blog, page)
    photos = getter.pictures(content.text, args.smallsizes)
    medias.extend(photos)

    if args.videos:
        vids = getter.videos(content.text)
        medias.extend(vids)

    return medias

def getmedia(dldir, media):
    retry_dl = True
    while retry_dl:
        try:
            tumblder.write.media(dldir, media, session)
            retry_dl = False
        except requests.exceptions.ConnectionError:
            print_log('download stalled: ', media, True)
            time.sleep(10)

def getmedias(args, medias):
    global STAT_new_medias

    for media in medias:
        try:
            getmedia(args.dldir, media)
        except tumblder.exceptions.FileExists as err:
            if not args.forceupdate:
                raise tumblder.exceptions.UpdateStopped(err.value)
            sys.stderr.write(str(err) + '\n')
        except tumblder.exceptions.StaticFileExists as err:
            pass
        else:
            STAT_new_medias += 1
        finally:
            sys.stderr.flush()

def browse(args):
    global STAT_new_medias

    blogname = regex.BLOGNAME.match(args.blog)
    if not blogname:
        return 1
    args.blog = blogname.group('protocol') + blogname.group('blogname') + regex.TUMBLR
    getter = import_module('tumblder.html') if args.html else import_module('tumblder.api')

    print(args.blog + ' ' + '=' * (40 - len(args.blog)))
    tumblder.write.prepare(args.dldir)
    try:
        for i in range(args.startpage, args.startpage + args.pagelimit):
            print('=== page ' + str(i))
            medias = pagemedias(args, i, getter)
            retry_dl = True
            getmedias(args, medias)
    except tumblder.exceptions.UpdateStopped as err:
        sys.stderr.write(str(err) + '\n')
    sys.stderr.flush()
    print('\nPages: {0}/{1}'.format(i, args.startpage + args.pagelimit - 1))
    print('New medias: {0}'.format(STAT_new_medias))
