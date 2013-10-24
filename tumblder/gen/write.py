# vim: expandtab tabstop=4 shiftwidth=4

import os

def write(directory, html, filename='index.html'):
    f = open(os.path.join(directory, filename), 'w')
    f.write(html)
    f.close()
