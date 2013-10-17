#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

from tumblder import session

def content(blog, page):
    return session.get(blog + '/api/read/?type=video&num=' + str(page * 20))

def videos(content):
    xml = session.get('')
