#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4
# -*- coding: utf-8 -*-

import time
import sys
import signal
import shutil
import os

from importlib import import_module
from threading import Thread

import requests

import tumblder.getter.html
import tumblder.write
import tumblder.exceptions
import tumblder.regex as regex
import tumblder.gen.html

from tumblder.pycommon.logging import print_log

session = requests.Session()

try:
    from Queue import Queue
    mediaqueue = Queue()
except ImportError:
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
        mediaqueue.put([media, page])

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
                print_log('download stalled {0}/{1}:'.format(retry_try, retry_max), media[0]['url'], True)
                time.sleep(10 * retry_try)
                retry_try += 1
        if retry_try > retry_max:
            print_log('download failed: ', media[0]['url'], True)
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
    while not tumblder.write.STOPWRITE:
        media = mediaqueue.get()
        fetchmedia(args, media)
        mediaqueue.task_done()
    while tumblder.write.STOPWRITE:
        try:
            mediaqueue.get_nowait()
            mediaqueue.task_done()
        except queue.Empty:
            pass

def sig_stop_dl(signum, frame):
    tumblder.write.STOPWRITE = True

def browse(args):
    global STAT_new_medias
    global STAT_page_medias

    tumblder.write.prepare(args.dldir)

    if args.fetch:
        blog = regex.BLOG.match(args.blog)

        if not blog:
            raise tumblder.exceptions.InvalidBlogUrl()

        args.blog = blog.group('protocol') + blog.group('name') + regex.TUMBLR
        getter = import_module('tumblder.getter.html')# if args.html else import_module('tumblder.getter.api')

        mediathread = Thread(target=fetcher, args=[args])
        mediathread.daemon = True
        mediathread.start()

        signal.signal(signal.SIGINT, sig_stop_dl)

        try:
            for i in range(args.startpage, args.startpage + args.pagelimit):
                if tumblder.write.STOPWRITE:
                    break
                lenmedias = pagemedias(args, i, getter)
                print_log('', '{0}, page {1}/{3}: {2} medias'.format(blog.group('name'),
                    i, lenmedias, args.startpage + args.pagelimit - 1), True)
            mediaqueue.join()
        except tumblder.exceptions.UpdateStopped as err:
            sys.stderr.write('{0}\n'.format(err))
            sys.stderr.flush()

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        print('{0}, new medias: {1}'.format(blog.group('name'), STAT_new_medias))

    if args.delete_small:
        photos = [x for x in os.listdir(args.dldir) if regex.ISPHOTO.match(x)]
        dphotos = tumblder.getter.html.purge_smallsizes(photos)
        for key, val in dphotos.items():
            try:
                if len(val['smallsizes']) > 0:
                    print(key, val['smallsizes'], val['type'])
                    for smallsize in val['smallsizes']:
                        os.remove(os.path.join(args.dldir, key) + '_' + str(smallsize) + '.' + val['type'])
            except KeyError:
                pass

    
    if args.generate:
        print('generating html pages: {0}'.format(args.dldir))
        pages = tumblder.gen.html.generate(args.dldir, root=args.root)
        for page in pages:
            tumblder.gen.html.write(args.dldir, page['html'], page['filename'])
        shutil.copy('jwplayer/jwplayer.html5.js', args.dldir)
        shutil.copy('jwplayer/jwplayer.flash.swf', args.dldir)
        shutil.copy('jwplayer/jwplayer.js', args.dldir)

