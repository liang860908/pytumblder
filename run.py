#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import argparse
import tumblder.download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blog', required=True)
    parser.add_argument('-f', '--dldir', default='./')
    parser.add_argument('-l', '--pagelimit', default='10', type=int)
    parser.add_argument('-o', '--open', action='store_true')
    parser.add_argument('-p', '--openin', default='firefox ')
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-s', '--smallsizes', action='store_true')
    parser.add_argument('-u', '--forceupdate', action='store_true')
    args = parser.parse_args()

    if args.recursive:
        print('/!\\ recursive download (take reblogs) not implemented /!\\')

    tumblder.download.browse(args)

if __name__ == '__main__':
    main()
