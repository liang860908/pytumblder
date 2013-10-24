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
import tumblder.gen.html
import tumblder.gen.write

from tumblder.common.logging import print_log

session = requests.Session()

STAT_new_medias = 0
STAT_page_medias = 0

def pagemedias(args, page, getter):
    medias = []

    content = getter.content(args.blog, page)
    photos = getter.pictures(content.text, args.smallsizes)
    medias.extend(photos)

    if args.videos:
        vids = getter.videos(content.text)
        medias.extend(vids)

    return medias, len(medias)

def fetchmedia(dldir, media):
    retry_max = 3
    retry_dl = True
    retry_try = 1
    while retry_dl and retry_try <= retry_max:
        try:
            tumblder.write.media(dldir, media, session)
            retry_dl = False
        except requests.exceptions.ConnectionError:
            print_log('download stalled {0}/{1}:'.format(retry_try, retry_max), media['url'], True)
            time.sleep(10 * retry_try)
            retry_try += 1
    if retry_try > retry_max:
        print_log('download failed: ', media['url'], True)
    print('')

def fetchmedias(args, medias):
    global STAT_new_medias

    for media in medias:
        try:
            fetchmedia(args.dldir, media)
        except tumblder.exceptions.FileExists as err:
            if not args.forceupdate:
                raise tumblder.exceptions.UpdateStopped(err.value)
        except tumblder.exceptions.StaticFileExists as err:
            pass
        else:
            STAT_new_medias += 1
        finally:
            sys.stderr.flush()

def browse(args):
    global STAT_new_medias
    global STAT_page_medias

    if args.fetch:
        blogname = regex.BLOGNAME.match(args.blog)

        if not blogname:
            raise tumblder.exceptions.InvalidBlogUrl()

        args.blog = blogname.group('protocol') + blogname.group('blogname') + regex.TUMBLR
        getter = import_module('tumblder.html')# if args.html else import_module('tumblder.api')

        tumblder.write.prepare(args.dldir)

        try:
            for i in range(args.startpage, args.startpage + args.pagelimit):
                medias, lenmedias = pagemedias(args, i, getter)
                print('{0}, page {1}/{3}: {2} medias'.format(blogname.group('blogname'),
                    i, lenmedias, args.startpage + args.pagelimit - 1))
                fetchmedias(args, medias)
        except tumblder.exceptions.UpdateStopped as err:
            sys.stderr.write('{0}\n'.format(err))
            sys.stderr.flush()

        print('{0}, new medias: {1}'.format(blogname.group('blogname'), STAT_new_medias))

    if args.generate:
        print('generating html page: {0}'.format(args.dldir))
        html = tumblder.gen.html.generate(args.dldir, root=args.root)
        tumblder.gen.write.write(args.dldir, html)

