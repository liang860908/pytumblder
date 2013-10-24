# vim: expandtab tabstop=4 shiftwidth=4

import os

def generate(directory):
    html = '<html><head></head><body>'
    files = os.listdir(directory)
    for tfile in files:
        html += '<img src="{0}"/>\n'.format(tfile)
    html += '</body></html>'
    return html
