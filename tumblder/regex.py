#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import re
from re import compile as rec

_PICTYPES = '|'.join(['png', 'jpg', 'jpeg', 'gif'])
TUMBLR = '.tumblr.com'

ISPHOTO = rec('.*\.(' + _PICTYPES + ')')

PHOTO = rec('(http[s]?://[a-z0-9\.]*(?:media|static)' + TUMBLR + '/(?!avatar|preview)[^ ]*\.(?:' + _PICTYPES + '))', re.I)
PHOTOSET = rec('(http[s]?://[^ ]*/photoset_iframe/[^ ]*/false)', re.I)
SIZEDPHOTO = rec('.*/(?P<name>.*_)(?P<size>[0-9]+)\.(' + _PICTYPES + ')', re.I)

VIDEO = rec(r'\\x22(http[s]?://[^ ]*' + TUMBLR + r'/video_file/([^ ]*))\\x22 type=\\x22video/([^ ]*)\\x22', re.I)

FILENAME = rec('http[s]?://.*/(?P<name>.*\..*)')
STATICRES = rec('[^ ]*static' + TUMBLR + '[^ ]*', re.I)

BLOG = rec('(?P<protocol>http[s]?://)(?P<name>.*)' + TUMBLR + '[/]?', re.I)
