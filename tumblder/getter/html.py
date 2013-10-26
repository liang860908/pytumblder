#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

from tumblder import session
import tumblder.regex as regex

def getcontent(blog, page):
    return session.get(blog + '/page/' + str(page))

def purge_smallsizes(photos):
    dphotos = {}
    for photo in photos:
        sizedphoto = regex.SIZEDPHOTO.match(photo)
        if sizedphoto:
            name = sizedphoto.group('name')
            size = int(sizedphoto.group('size'))
            if name in dphotos.keys():
                if dphotos[name]['size'] < size:
                    dphotos[name]['size'] = size
                    dphotos[name]['url'] = photo
            else:
                dphotos[name] = {'size':size, 'url':photo}
        else:
            dphotos[photo] = {'url':photo, 'size':0}
    photos = []
    for val in dphotos.values():
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
