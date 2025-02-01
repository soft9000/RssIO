#!/usr/bin/env python3
# RssIO.py: A friendly, neighborhood RSS feed reader / writer.
# Rev 1.03
# Status: Ready for prime time.

# 2025/01/21: Created + shared at https://github.com/soft9000/RssIO
# 2025/01/22: Added support for channel <generator/>
# 2025/01/23: Unified re-usage. Common verifications.

# CAVEAT: Whilst pubDates are not required, when not present pubDates will be 
# slapped 'oer every channel and item within every feed / item therein. 
# It's a feature / feel free to update your final as required.

import os
import os.path
import time
from datetime import datetime
import email.utils

import xml.etree.ElementTree as ET

from RssExceptions import RssException
from RssItemSecured import RSSItemSecured

from RssItemMeta import RSSItemMeta


class RSSFeed(RSSItemMeta):
    this_project = 'https://github.com/soft9000/RssIO'

    def __init__(self, title, description, link, date_str=time.ctime()):
        super().__init__(title, description, link, date_str)
        self._generator = RSSFeed.this_project
        self._items = []

    def is_robust(self):
        ''' A simple test to see if the feed header is ready for prime time.'''
        return self._title and self._link and self._description

    def use_default_generator(self):
        ''' Use the default project string as the generator tag.'''
        self.generator = RSSFeed.this_project
    
    def try_pubDate(self, date_str)->bool:
        ''' Attempt to set the pubDate. Return True if successful.'''
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self._pubDate = date_str
            return True
        except:
            return False

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, value):
        self._generator = value

    def add_item(self, item)->bool:
        ''' Add an ROBUST item to the feed. Returns False if the item is not robust.'''
        if not item or not item.is_robust():
            return False
        self._items.append(item)
        return True

    def to_string(self):
        '''Converts an entire RSS feed - channel as well as any topics - to a string.'''
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        ET.SubElement(channel, 'title').text = self._title
        ET.SubElement(channel, 'link').text = self._link
        ET.SubElement(channel, 'description').text = self._description
        ET.SubElement(channel, 'generator').text = self._generator
        ET.SubElement(channel, 'pubDate').text = self._pubDate
        for item in self._items:
            item_elem = ET.SubElement(channel, 'item')
            ET.SubElement(item_elem, 'title').text = item.title
            ET.SubElement(item_elem, 'link').text = item.link
            ET.SubElement(item_elem, 'description').text = item.description
            ET.SubElement(item_elem, 'pubDate').text = item.pubDate
        tree = ET.ElementTree(rss)
        rough_string = ET.tostring(tree.getroot(), 'utf-8')
        import xml.dom.minidom
        parsed_string = xml.dom.minidom.parseString(rough_string)
        return parsed_string.toprettyxml(indent="  ")
    
    @staticmethod
    def load(filename):
        '''Loads an entire RSS feed - channel as well as any topics - from a file.'''
        feed = RSSFeed(None, None, None)
        if not os.path.exists(filename):
            return None
        tree = ET.parse(filename)
        root = tree.getroot()
        feed._title = root.find('channel/title').text
        feed._link = root.find('channel/link').text
        feed._description = root.find('channel/description').text

        generator = root.find('channel/generator')
        if generator is not None:
            feed._generator = generator.text

        feed._pubDate = root.find('channel/pubDate')
        if feed._pubDate is None:
            feed._pubDate = time.ctime()    # use today's date
        else:
            feed._pubDate = feed.pubDate.text

        feed._items = []
        for item in root.findall('channel/item'):
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            pubDate = item.find('pubDate')
            if pubDate is None:
                feed._items.append(RSSItemMeta(title, link, description)) # use today's date
            else:
                feed._items.append(RSSItemMeta(title, link, description, pubDate.text))
        return feed

    @staticmethod
    def save(feed, filename):
        '''Saves an entire RSS feed - channel as well as any topics - to a file.'''
        feed.use_default_generator()
        xstring = RSSFeed.to_string(feed)
        with open(filename, 'w') as f:
            f.write(xstring)
        return True


def test_cases(debug=False):
    print(f"***** Testing Module {__name__}.")
    # The legacy file is to be added to:
    legacy_rss = "./RssIO/nexus.rss"
    myFeed = RSSFeed.load(legacy_rss)
    if myFeed is None:
        myFeed = RSSFeed.load("nexus.rss")
    if myFeed is None:
        raise RssException("Failed to load the feed.")

    if os.path.exists("testing.rss"):
        os.unlink("testing.rss")

    RSSFeed.save(myFeed, "testing.rss")
    myFeed.use_default_generator()
    if debug:
        print(myFeed.to_string())

    if myFeed.is_robust():
        print("Feed is robust.")

    if not debug and os.path.exists("testing.rss"):
        os.unlink("testing.rss")
    
    print("Testing Success.")


if __name__ == '__main__':
    test_cases()
