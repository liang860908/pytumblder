#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import argparse
import tumblder.worker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blog', required=True,
            help='full url to tumblr blog. http://blog.tumblr.com')
    parser.add_argument('-f', '--dldir', default='.',
            help='download directory')
    parser.add_argument('-l', '--pagelimit', default=1, type=int,
            help='number of pages to watch')
    parser.add_argument('-s', '--smallsizes', action='store_true',
            help='take small and full size photos')
    parser.add_argument('-u', '--forceupdate', action='store_true',
            help='look each page for un update, instead of stopping on the first already-downloaded media')
    parser.add_argument('-F', '--fetch', action='store_true',
            help='fetch pages and medias')
    parser.add_argument('-G', '--generate', action='store_true',
            help='generate HTML index page')
    parser.add_argument('-H', '--html', action='store_false',
            help='dont use the api, parse HTML like a browser can do')
    parser.add_argument('-R', '--root', type=str, default='',
            help='in generated html, take this as root')
    parser.add_argument('-S', '--startpage', default=1, type=int,
            help='start browsing from this page number')
    parser.add_argument('-V', '--videos', action='store_true',
            help='download videos too')
    args = parser.parse_args()

    res = tumblder.worker.browse(args)
    if res == 1:
        print('Bad blog url. Example: http://blog.tumblr.com')

if __name__ == '__main__':
    main()
