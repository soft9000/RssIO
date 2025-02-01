#!/usr/bin/env python3
# RssExceptions.py: Exceptional situations.
# Rev 1.0
# Status: Production.

class RssException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    