#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import time
import sys

from importlib import import_module
from threading import Thread

import requests

import tumblder.write
import tumblder.exceptions
import tumblder.regex as regex
import tumblder.gen.html
import tumblder.gen.write

from tumblder.pycommon.logging import print_log

session = requests.Session()

try:
    mediaqueue = Queue()
except NameError:
    import queue
    mediaqueue = queue.Queue()

STAT_new_medias = 0
STAT_page_medias = 0

def pagemedias(args, page, getter):
    medias = []

    content = getter.getcontent(args.blog, page)
    photos = getter.pictures(content.text, args.smallsizes)
    medias.extend(photos)

    if args.videos:
        vids = getter.videos(content.text)
        medias.extend(vids)

    for media in medias:
        mediaqueue.put(media)

    return len(medias)

def fetchmedia(args, media):
    global STAT_new_medias

    try:
        retry_max = 3
        retry_dl = True
        retry_try = 1
        while retry_dl and retry_try <= retry_max:
            try:
                tumblder.write.media(args.dldir, media)
                retry_dl = False
            except requests.exceptions.ConnectionError:
                print_log('download stalled {0}/{1}:'.format(retry_try, retry_max), media['url'], True)
                time.sleep(10 * retry_try)
                retry_try += 1
        if retry_try > retry_max:
            print_log('download failed: ', media['url'], True)
        print('')
    except tumblder.exceptions.FileExists as err:
        if not args.forceupdate:
            raise tumblder.exceptions.UpdateStopped(err.value)
    except tumblder.exceptions.StaticFileExists as err:
        pass
    else:
        STAT_new_medias += 1
    finally:
        sys.stderr.flush()

def fetcher(args):
    while True:
        media = mediaqueue.get()
        fetchmedia(args, media)
        mediaqueue.task_done()

def browse(args):
    global STAT_new_medias
    global STAT_page_medias

    if args.fetch:
        blog = regex.BLOG.match(args.blog)

        if not blog:
            raise tumblder.exceptions.InvalidBlogUrl()

        args.blog = blog.group('protocol') + blog.group('name') + regex.TUMBLR
        getter = import_module('tumblder.html')# if args.html else import_module('tumblder.api')

        tumblder.write.prepare(args.dldir)

        mediathread = Thread(target=fetcher, args=[args])
        mediathread.daemon = True
        mediathread.start()

        try:
            for i in range(args.startpage, args.startpage + args.pagelimit):
                lenmedias = pagemedias(args, i, getter)
                print('{0}, page {1}/{3}: {2} medias'.format(blog.group('name'),
                    i, lenmedias, args.startpage + args.pagelimit - 1))
            mediaqueue.join()
        except tumblder.exceptions.UpdateStopped as err:
            sys.stderr.write('{0}\n'.format(err))
            sys.stderr.flush()

        print('{0}, new medias: {1}'.format(blog.group('name'), STAT_new_medias))

    if args.generate:
        print('generating html page: {0}'.format(args.dldir))
        html = tumblder.gen.html.generate(args.dldir, root=args.root)
        tumblder.gen.write.write(args.dldir, html)

