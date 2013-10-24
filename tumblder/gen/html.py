# vim: expandtab tabstop=4 shiftwidth=4

import os

from tumblder import regex

def generate(directory, root=''):
    css = '''<style media="screen" type="text/css">
    img {
        max-width: 500px;
        max-height: 640px;
    }
    </style>'''
    html = '<html><head>{0}</head><body>'.format(css)
    files = reversed(sorted(os.listdir(directory)))
    photos = [x for x in files if regex.ISPHOTO.match(x)]
    for photo in photos:
        src = os.path.join(root, photo)
        html += '<a href="{0}"><img src="{0}" /></a>\n'.format(src)
    html += '</body></html>'
    return html
