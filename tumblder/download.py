#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import os
import time

import requests

import tumblder.regex

session = requests.Session()

STAT_photos = 0
STAT_new_photos = 0

def store(subdir, url):
    filename = tumblder.regex.FILENAME.match(url).group(1)
    msgurl = ' (' + url + ')'
    filepath = subdir + '/' + filename

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    fileexists = os.path.exists(filepath)

    if tumblder.regex.STATICPHOTO.match(url) and fileexists:
        print('static photo: ' + filename + msgurl)
        return 2
    if fileexists:
        print('already downloaded: ' + filename + msgurl)
        return 1

    datas = None
    while True:
        try:
            datas = session.get(url).content
            print('downloading: ' + filename + msgurl)
            break
        except requests.exceptions.ConnectionError:
            print('Sleeping for 10 seconds...')
            time.sleep(10)

    f = open(subdir + '/' + filename, 'wb')
    f.write(datas)
    f.close()

    return 0

def purge_smallsizes(photos):
    dphotos = {}
    for photo in photos:
        m = tumblder.regex.SIZEDPHOTO.match(photo)
        if m:
            name = m.group(1)
            size = int(m.group(2))
            ext = m.group(3)
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

def medias(content, smallsizes):
    photos = tumblder.regex.PHOTO.findall(content)
    plentyphotos = tumblder.regex.PHOTOSET.findall(content)

    for plentyphoto in plentyphotos:
        extend = tumblder.regex.PHOTO.findall(session.get(plentyphoto).text)
        photos.extend(extend)
    photos = list(set(photos))

    if not smallsizes:
        photos = purge_smallsizes(photos)

    return photos

def pagework(args, page):
    global STAT_photos
    global STAT_new_photos
    url = args.blog + '/page/' + page
    content = session.get(url)
    print('page ' + page)
    photos = medias(content.text, args.smallsizes)
    for photo in photos:
        res = store(args.dldir, photo)
        if res == 2:
            pass
        elif res == 0:
            STAT_photos += 1
            STAT_new_photos += 1
        elif res == 1 and not args.forceupdate:
            return 1
        elif res == 1:
            STAT_photos += 1
        if args.open:
            os.system(args.openin + ' ' + photo)

def browse(args):
    global STAT_photos
    global STAT_new_photos

    for i in range(1, args.pagelimit + 1):
        res = pagework(args, str(i))
        if res == 1:
            break
    print('Resume:')
    print('Pages: {0}/{1}'.format(i, args.pagelimit))
    print('Photos: {0}'.format(STAT_photos))
    print('New photos: {0}'.format(STAT_new_photos))
