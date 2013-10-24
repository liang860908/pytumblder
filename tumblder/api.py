#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

from tumblder import session

def getcontent(blog, page, mediatype):
    return session.get('{0}/api/read/?type={1}&num={2}'.format(blog, mediatype, str(page * 20)))

def videos(content):
    pass
