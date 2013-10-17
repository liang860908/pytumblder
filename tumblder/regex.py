#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import re
from re import compile as rec


_PICTYPES = '|'.join(['png', 'jpg', 'jpeg', 'gif'])
TUMBLR = '.tumblr.com'

PHOTO = rec('(http[s]?://[a-z0-9\.]*(?:media|static)' + TUMBLR + '/(?!avatar|preview)[^ ]*\.(?:' + _PICTYPES + '))', re.I)
PHOTOSET = rec('(http[s]?://[^ ]*/photoset_iframe/[^ ]*/false)', re.I)
SIZEDPHOTO = rec('.*/(.*_)([0-9]+)\.(' + _PICTYPES + ')', re.I)

VIDEO = rec(r'\\x22(http[s]?://[^ ]*' + TUMBLR + '/video_file/([^ ]*))\\x22 type=\\x22video/([^ ]*)\\x22', re.I)

FILENAME = rec('http[s]?://.*/(.*\..*)')
STATICRES = rec('[^ ]*static' + TUMBLR + '[^ ]*', re.I)

BLOGNAME = rec('(?P<protocol>http[s]?://)(?P<blogname>.*)' + TUMBLR + '[/]?', re.I)
