#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4
# -*- coding: utf-8 -*-

from tumblder import session
import tumblder.regex as regex

def getcontent(blog, page):
    return session.get(blog + '/page/' + str(page))

def purge_smallsizes(photos):
    dphotos = {}
    for photo in photos:
        sizedphoto = regex.SIZEDPHOTO.match(photo)
        pictype = regex.ISPHOTO.match(photo).group('type')
        if sizedphoto:
            name = sizedphoto.group('name')
            size = int(sizedphoto.group('size'))
            try:
                if size > dphotos[name]['size']:
                    try:
                        dphotos[name]['smallsizes'] = [dphotos[name]['size']]
                    except KeyError:
                        dphotos[name]['smallsizes'].append(dphotos[name]['size'])
                    dphotos[name]['size'] = size
                    dphotos[name]['url'] = photo
                elif size < dphotos[name]['size']:
                    try:
                        dphotos[name]['smallsizes'] = [size]
                    except KeyError:
                        dphotos[name]['smallsizes'].append(size)
            except KeyError:
                dphotos[name] = {'size':size, 'url':photo}
            dphotos[name]['type'] = pictype
        else:
            dphotos[photo] = {'url':photo, 'size':0}
            dphotos[photo]['type'] = pictype

    return dphotos

def pictures(content, smallsizes):
    photos = regex.PHOTO.findall(content)
    iframephotos = regex.PHOTOSET.findall(content)

    ldphotos = []

    for iframephoto in iframephotos:
        extend = regex.PHOTO.findall(session.get(iframephoto).text)
        photos.extend(extend)
    photos = list(set(photos))

    if not smallsizes:
        photos = [x['url'] for x in purge_smallsizes(photos).values()]

    for photo in photos:
        filename = regex.FILENAME.match(photo).group('name')
        ldphotos.append({'url':photo, 'name':filename})

    return ldphotos

def videos(content):
    vids = regex.VIDEO.findall(content)
    ldvids = []
    for vid in vids:
        vidurl = vid[0]
        vidname = vid[1].replace('/', '_') + '.' + vid[2]
        ldvids.append({'url':vidurl, 'name':vidname})
    return ldvids
