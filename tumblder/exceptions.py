#!/usr/bin/env python
# vim: expandtab tabstop=4 shiftwidth=4

class FileExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'file exists: ' + repr(self.value)

class StaticFileExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'static file exists: ' + repr(self.value)

class UpdateStopped(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'update stopped: ' + repr(self.value)

class DownloadPaused(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'download paused: ' + repr(self.value)
