#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import re
from re import compile as rec

_PICTYPES = r'|'.join([r'png', r'jpg', r'jpeg', r'gif'])
_VIDTYPES = r'|'.join([r'mp4'])
TUMBLR = r'.tumblr.com'

ISPHOTO = rec(r'.*\.(?P<type>' + _PICTYPES + ')')
ISVIDEO = rec(r'.*\.(?P<type>' + _VIDTYPES + ')')

PHOTO = rec(r'(http[s]?://[a-z0-9\.]*(?:media|static)' + TUMBLR + r'/(?:[^ /]*/?)tumblr_[^ ]*\.(?:' + _PICTYPES + r'))', re.I)
PHOTOSET = rec(r'(http[s]?://[^ ]*/photoset_iframe/[^ ]*/false)', re.I)
SIZEDPHOTO = rec(r'.*[/]?(?P<name>tumblr_.*)_(?P<size>[0-9]+)\.(?P<type>' + _PICTYPES + r')', re.I)

VIDEO = rec(r'\\x22(http[s]?://[^ ]*' + TUMBLR + r'/video_file/([^ ]*))\\x22 type=\\x22video/(' + _VIDTYPES + r')\\x22', re.I)

FILENAME = rec(r'http[s]?://.*/(?P<name>.*\..*)')
STATICRES = rec(r'[^ ]*static' + TUMBLR + r'[^ ]*', re.I)

BLOG = rec(r'(?P<protocol>http[s]?://)(?P<name>.*)' + TUMBLR + r'[/]?', re.I)
