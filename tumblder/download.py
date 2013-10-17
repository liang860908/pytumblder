#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import time
import sys

import requests

import tumblder.write
import tumblder.exceptions
from tumblder import regex

session = requests.Session()

STAT_new_medias = 0

def purge_smallsizes(photos):
    dphotos = {}
    for photo in photos:
        m = regex.SIZEDPHOTO.match(photo)
        if m:
            name = m.group(1)
            size = int(m.group(2))
            if name in dphotos.keys():
                if dphotos[name]['size'] < size:
                    dphotos[name]['size'] = size
                    dphotos[name]['url'] = photo
            else:
                dphotos[name] = {'size':size, 'url':photo}
        else:
            dphotos[photo] = {'url':photo, 'size':0}
    photos = []
    for key, val in dphotos.items():
        photos.append(val['url'])

    return photos

def pictures(content, smallsizes):
    photos = regex.PHOTO.findall(content)
    iframephotos = regex.PHOTOSET.findall(content)

    ldphotos = []

    for iframephoto in iframephotos:
        extend = regex.PHOTO.findall(session.get(iframephoto).text)
        photos.extend(extend)
    photos = list(set(photos))

    if not smallsizes:
        photos = purge_smallsizes(photos)

    for photo in photos:
        filename = regex.FILENAME.match(photo).group(1)
        ldphotos.append({'url':photo, 'name':filename})

    return ldphotos

def videos(content):
    vids = regex.VIDEO.findall(content)
    ldvids = []
    for vid in vids:
        ldvids.append({'url':vid[0], 'name':vid[1].replace('/', '_') + '.' + vid[2]})
    return ldvids

def pagework(args, page):
    global STAT_new_medias
    url = args.blog + '/page/' + page
    content = session.get(url)
    tumblder.write.prepare(args.dldir)

    medias = []
    photos = pictures(content.text, args.smallsizes)
    medias.extend(photos)
    if args.videos:
        vids = videos(content.text)
        medias.extend(vids)

    for media in medias:
        try:
            res = tumblder.write.media(args.dldir, media, session)
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

        if args.open:
            os.system(args.openin + ' ' + media)

def browse(args):
    global STAT_new_medias

    blogname = regex.BLOGNAME.match(args.blog)
    if not blogname:
        return 1
    args.blog = blogname.group('protocol') + blogname.group('blogname') + regex.TUMBLR

    print(args.blog + ' ' + '=' * (40 - len(args.blog)))
    try:
        for i in range(args.startpage, args.startpage + args.pagelimit):
            print('=== page ' + str(i))
            res = pagework(args, str(i))
    except tumblder.exceptions.UpdateStopped as err:
        sys.stderr.write(str(err) + '\n')
    sys.stderr.flush()
    print('\nPages: {0}/{1}'.format(i, args.startpage + args.pagelimit - 1))
    print('New medias: {0}'.format(STAT_new_medias))
