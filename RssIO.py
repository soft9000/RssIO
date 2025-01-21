#!/usr/bin/env python3
# RssIO.py: A friendly, neighborhood RSS feed reader / writer.
# Shared 2025/01/21 by Randall Nagy
# Rev 1.0

# CAVEAT: Whilst pubDates are not required, when not present pubDates will be 
# slapped 'oer every channel and item within every feed / item therein. 
# It's a feature / feel free to update your final as required.

import time
from datetime import datetime
import email.utils

import xml.etree.ElementTree as ET

class RSSItem:
    def __init__(self, title, link, description, date_str=time.ctime()):
        self._title = title
        self._link = link
        self._description = description
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self._pubDate = date_str
        except:
            self._pubDate = time.ctime()

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


class RSSFeed:
    def __init__(self, title, link, description, date_str=time.ctime()):
        self._title = title
        self._link = link
        self._description = description
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self._pubDate = date_str
        except:
            self._pubDate = time.ctime()
        self._items = []

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

    def add_item(self, item):
        self._items.append(item)


    def to_string(self):
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        ET.SubElement(channel, 'title').text = self._title
        ET.SubElement(channel, 'link').text = self._link
        ET.SubElement(channel, 'description').text = self._description
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
        feed = RSSFeed(None, None, None)
        tree = ET.parse(filename)
        root = tree.getroot()
        feed._title = root.find('channel/title').text
        feed._link = root.find('channel/link').text
        feed._description = root.find('channel/description').text
        feed._pubDate = root.find('channel/pubDate')
        if not feed.pubDate:
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
                feed._items.append(RSSItem(title, link, description)) # use today's date
            else:
                feed._items.append(RSSItem(title, link, description, pubDate.text))
        return feed

    @staticmethod
    def save(feed, filename):
        xstring = RSSFeed.to_string(feed)
        with open(filename, 'w') as f:
            f.write(xstring)


if __name__ == '__main__':
    myFeed = RSSFeed.load(r"C:\d_drive\USR\sites\aws.2024\Soft9000.rnd\nexus.rss")
    # RSSFeed.save(myFeed, r"C:\d_drive\USR\sites\aws.2024\Soft9000.rnd\testing.rss")
    print(myFeed.to_string())
