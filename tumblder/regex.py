#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

import re
from re import compile as rec


_PICTYPES = '|'.join(['png', 'jpg', 'jpeg', 'gif'])

PHOTO = rec('(http[s]?://[a-z0-9\.]*(?:media|static).tumblr.com/(?!avatar|preview).*\.(?:' + _PICTYPES + '))', re.I)
PHOTOSET = rec('(http[s]?://.*/photoset_iframe/.*/false)', re.I)
STATICPHOTO = rec('.*static.tumblr.com.*', re.I)
SIZEDPHOTO = rec('.*/(.*_)([0-9]+)\.(' + _PICTYPES + ')', re.I)

FILENAME = rec('http[s]?://.*/(.*\..*)')
