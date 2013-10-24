# vim: expandtab tabstop=4 shiftwidth=4

import os

from tumblder import regex

def generate(directory, root=''):
    html = '<html><head></head><body>'
    photos = [x for x in sorted(os.listdir(directory)) if regex.ISPHOTO.match(x)]
    for photo in photos:
        src = os.path.join(root, photo)
        html += '<a href="{0}"><img src="{0}" width="500" /></a>\n'.format(src)
    html += '</body></html>'
    return html
