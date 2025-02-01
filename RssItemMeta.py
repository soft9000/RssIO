import time
import email.utils

class RSSItemMeta:
    def __init__(self, title, description, link, date_str=time.ctime()):
        self._title = title
        self._link = link
        self._description = description
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self._pubDate = date_str
        except:
            self._pubDate = time.ctime()

    def is_robust(self):
        ''' A simple test to see if the item is ready for prime time.'''
        return self._title and self._link and self._description
   
    def try_pubDate(self, date_str)->bool:
        ''' Attempt to set the pubDate. Return True if successful.'''
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self._pubDate = date_str
            return True
        except:
            return False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def pubDate(self):
        return self._pubDate

    @pubDate.setter
    def pubDate(self, value):
        self._pubDate = value