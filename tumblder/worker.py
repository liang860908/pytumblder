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
    retry_max = 3
    retry_dl = True
    retry_try = 0
    while retry_dl and retry_try < retry_max:
        try:
            tumblder.write.media(dldir, media, session)
            retry_dl = False
        except requests.exceptions.ConnectionError:
            retry_try += 1
            print_log('download stalled {0}/{1}:'.format(retry_try, retry_max), media, True)
            time.sleep(10 * retry_try)
    if not retry_try < retry_max:
        print_log('download failed: ', media, True)
    print('')

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
