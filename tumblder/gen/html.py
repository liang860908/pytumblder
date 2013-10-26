# vim: expandtab tabstop=4 shiftwidth=4

import os

from tumblder import regex

def generate(directory, root=''):
    pages = []
    files = sorted(os.listdir(directory))
    photos = [x for x in files if regex.ISPHOTO.match(x)]
    photos_per_page = 8
    pagenum = 0
    pagemax = int(len(photos) / photos_per_page) - 1
    imgwidth = str(int(100 / (photos_per_page / 2 + 1)))

    css = '''<style media="screen" type="text/css">
    img {
        width: ''' + imgwidth + '''%;
    }
    p {
        margin: auto;
        text-align: center;
    }
    #navigator {
        margin-bottom: 10px;
    }
    #photos {
        max-height: 90%;
    }
    </style>'''

    for i in range(0, len(photos), photos_per_page):
        photoset = photos[i:(i + photos_per_page)]
        precpage = pagenum - 1 if i > 0 else 0
        nextpage = pagenum + 1 if pagenum < pagemax else pagemax
        html = '<!DOCTYPE html>\n'
        html += '<html><head>{0}<meta charset="utf-8"></head><body>\n'.format(css)
        nav = '<p id="navigator">'
        nav += '<a href="index0.html">Début</a> '
        nav += '— <a href="index{0}.html">précédent</a> | '.format(precpage) 
        nav += '<a href="index{0}.html">suivant</a> — '.format(nextpage) 
        nav += '<a href="index{0}.html">Fin</a>'.format(pagemax)
        nav += '</p>\n'
        html += nav
        html += '<p id="photos">\n'
        for photo in photoset:
            src = os.path.join(root, photo)
            html += '<a href="{0}"><img src="{0}"></a>\n'.format(src)
        html += '</p>\n'
        html += nav
        html += '</body></html>'
        pages.append(html)
        pagenum += 1
    return pages
