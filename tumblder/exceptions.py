#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

class InvalidBlogUrl(Exception):
    def __str__(self):
        return 'invalid blog url'

class FileExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'file exists: {0}'.format(repr(self.value))

class StaticFileExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'static file exists: {0}'.format(repr(self.value))

class UpdateStopped(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'update stopped: {0}'.format(repr(self.value))
