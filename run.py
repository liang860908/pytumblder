#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import argparse
import tumblder.download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blog', required=True,
            help='full url to tumblr blog. http://blog.tumblr.com')
    parser.add_argument('-f', '--dldir', default='./',
            help='download directory')
    parser.add_argument('-l', '--pagelimit', default=1, type=int,
            help='number of pages to watch')
    parser.add_argument('-o', '--open', action='store_true',
            help='open in a program. change with --openin')
    parser.add_argument('-p', '--openin', default='firefox ',
            help='open in this program')
    parser.add_argument('-s', '--smallsizes', action='store_true',
            help='take small and full size photos')
    parser.add_argument('-u', '--forceupdate', action='store_true',
            help='look each page for un update, instead of stopping on the first already-downloaded media')
    parser.add_argument('-S', '--startpage', default=1, type=int,
            help='start browsing from this page number')
    parser.add_argument('-V', '--videos', action='store_true',
            help='download videos too')
    args = parser.parse_args()

    res = tumblder.download.browse(args)
    if res == 1:
        print('Bad blog url. Example: http://blog.tumblr.com')

if __name__ == '__main__':
    main()
