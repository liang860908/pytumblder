# vim: expandtab tabstop=4 shiftwidth=4

import os

def generate(directory, root=''):
    html = '<html><head></head><body>'
    files = os.listdir(directory)
    for tfile in files:
        html += '<img src="{0}"/>\n'.format(os.path.join(root, tfile))
    html += '</body></html>'
    return html
