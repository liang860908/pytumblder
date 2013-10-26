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
    files = reversed(sorted(os.listdir(directory)))
    photos = [x for x in files if regex.ISPHOTO.match(x)]
    pagenum = 0
    for i in range(0, len(photos), 10):
        photoset = photos[i:(i+10)]
        html = '<!DOCTYPE html><html><head>{0}<meta charset="utf-8"></head><body>'.format(css)
        html += '<p id="navigator">— <a href="index{0}.html">précédent</a>'.format(pagenum - 1) 
        html += ' | '
        html += '<a href="index{0}.html">suivant</a> —'.format(pagenum + 1) 
        html += '</p><p>'
        for photo in photoset:
            src = os.path.join(root, photo)
            html += '<a href="{0}"><img src="{0}" /></a>\n'.format(src)
        html += '</p></body></html>'
        pages.append(html)
        pagenum += 1
    return pages
