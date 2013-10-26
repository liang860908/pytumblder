# vim: expandtab tabstop=4 shiftwidth=4

import os

from tumblder import regex

def generate(directory, root=''):
    css = '''<style media="screen" type="text/css">
    img {
        max-width: 300px;
        max-height: 300px;
    }
    p {
        margin: auto;
        text-align: center;
    }
    #navigator {
        margin-bottom: 10px;
    }
    </style>'''
    pages = []
    files = sorted(os.listdir(directory))
    photos = [x for x in files if regex.ISPHOTO.match(x)]
    photos_per_page = 10
    pagenum = 0
    pagemax = int(len(photos) / photos_per_page) - 1
    for i in range(0, len(photos), photos_per_page):
        photoset = photos[i:(i+10)]
        precpage = pagenum - 1 if i > 0 else 0
        nextpage = pagenum + 1 if pagenum < pagemax else pagemax
        html = '<!DOCTYPE html>\n'
        html += '<html><head>{0}<meta charset="utf-8"></head><body>\n'.format(css)
        html += '<p id="navigator">'
        html += '<a href="index0.html">Début</a>'
        html += '— <a href="index{0}.html">précédent</a>'.format(precpage) 
        html += ' | '
        html += '<a href="index{0}.html">suivant</a> —'.format(nextpage) 
        html += '<a href="index{0}.html">Fin</a>'.format(pagemax)
        html += '</p><p>\n'
        for photo in photoset:
            src = os.path.join(root, photo)
            html += '<a href="{0}"><img src="{0}" /></a>\n'.format(src)
        html += '</p></body></html>'
        pages.append(html)
        pagenum += 1
    return pages
