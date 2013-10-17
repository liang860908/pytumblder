#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

from tumblder import session
import tumblder.regex as regex

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
