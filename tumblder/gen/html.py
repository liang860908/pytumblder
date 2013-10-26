# vim: expandtab tabstop=4 shiftwidth=4

import os

from tumblder import regex

def write(directory, html, filename='index.html'):
    fhtml = open(os.path.join(directory, filename), 'w')
    fhtml.write(html)
    fhtml.close()

def generate(directory, root=''):
    pages = []
    files = sorted(os.listdir(directory))
    photos = [x for x in files if regex.ISPHOTO.match(x)]
    videos = [x for x in files if regex.ISVIDEO.match(x)]
    medias = photos + videos
    lenmedias = len(photos) + len(videos)
    medias_per_page = 8
    pagenum = 0
    pagemax = int(lenmedias / medias_per_page) - 1
    zerofill = len(str(pagemax))
    imgwidth = str(int(100 / (medias_per_page / 2 + 1)))

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
    #medias {
        max-height: 90%;
    }
    </style>'''

    for i in range(0, len(medias), medias_per_page):
        mediaset = medias[i:(i + medias_per_page)]
        precpage = pagenum - 1 if i > 0 else 0
        nextpage = pagenum + 1 if pagenum < pagemax else pagemax
        html = '<!DOCTYPE html>\n'
        html += '<html><head>{0}<meta charset="utf-8"></head><body>\n'.format(css)
        nav = '<p id="navigator">'
        nav += '<a href="index{0}.html">Début</a> '.format(str(0).zfill(zerofill))
        nav += '— <a href="index{0}.html">précédent</a> | '.format(str(precpage).zfill(zerofill))
        nav += '<a href="index{0}.html">suivant</a> — '.format(str(nextpage).zfill(zerofill))
        nav += '<a href="index{0}.html">Fin</a>'.format(str(pagemax).zfill(zerofill))
        nav += '</p>\n'
        html += nav
        html += '<p id="medias">\n'
        for media in mediaset:
            src = os.path.join(root, media)
            if regex.ISPHOTO.match(media):
                html += '<a href="{0}"><img src="{0}"></a>\n'.format(src)
            elif regex.ISVIDEO.match(media):
                html += '<a href="{0}"><video src="{0}"></video></a>\n'.format(src)
        html += '</p>\n'
        html += nav
        html += '</body></html>'
        pages.append({'filename': 'index{0}.html'.format(str(pagenum).zfill(zerofill)), 'html': html})
        pagenum += 1
    return pages
