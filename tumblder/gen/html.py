# vim: expandtab tabstop=4 shiftwidth=4

import os

def generate(directory, root=''):
    html = '<html><head></head><body>'
    files = os.listdir(directory)
    for tfile in files:
        src = os.path.join(root, tfile)
        html += '<a href="{1}"><img src="{0}"/></a>\n'.format(src, src)
    html += '</body></html>'
    return html
