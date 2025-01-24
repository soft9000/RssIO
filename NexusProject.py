#! /usr/bin/env python3
#!/usr/bin/env python3
# NexusProject.py: Manage a site's RSS feed, templates, and more.
# Rev 0.01
# Status: R&D.

# 2025/01/24: Created + shared at https://github.com/soft9000/RssIO
from RssIO import *
from RssNexus import *
from TopicTemplate import TopicFile

class RssSite:
    PREFIX = '[HTML prefix usually here - braces not required.]'
    SUFFIX = '[HTML suffix usually here - braces not required.]'
    
    RSS_NODE = FileTypes.DEFAULT_RSS

    def __init__(self, root_folder, site_url):
        self.home_dir = root_folder
        self.url = site_url
        self.rss_file = self.home_dir + '/' + RssSite.RSS_NODE
        nexus_folder = NexusFolder()
        nexus_folder.assign('input', 'output', 'templates')
        default_template = nexus_folder.template_dir + '/default.txt'
        self.nexus = RSSNexus(nexus_folder, RssTemplateFile(default_template))

    def exists(self)->bool:
        if not os.path.exists(self.home_dir): 
            return False
        return self.nexus.exists()
    
    def create(self)->bool:
        '''Assert site folders, default template, and a default RSS feed.'''
        if not os.path.exists(self.home_dir): 
            os.mkdir(self.home_dir)             # create root folder
        if not self.nexus.exists():
            if not self.nexus.create():         # create input, output, and template folders
                return False
        if not self.nexus.template.exists():    # create default template file
            if not self.nexus.template.create_template_file(RssSite.PREFIX, RssSite.SUFFIX):
                return False
        rss_feed = RSSFeed("Channel / Site Title", "Description of this RSS channel or site", self.self.url + '/' + RssSite.RSS_NODE)
        if not rss_feed.exists():
            if not RSSFeed.save(rss_feed):      # create the default RSS Channel
                return False
        return True
    
    def update(self)->bool:
        '''Update the RSS feed.'''
        feed = RssSite.read_feed(self.rss_file)
        if not feed:
            return False
        for file in os.listdir(self.nexus.input_dir):
            if file.endswith(TopicFile.FILE_TYPE):
                # TODO: Get the meta from the topic / json file.
                topic = TopicFile.load(self.nexus.input_dir + '/' + file)
                if topic:
                    item = RSSItem(topic.title, topic.description, topic.url, topic.date)
                    feed.add_item(item)
                # TODO: Merge the template with the input topic.
                # TODO: Update the RSS folder to refer to merged output.
        return RSSFeed.save(feed)

    @staticmethod
    def read_feed(self, rss_file:str)->RSSFeed:
        '''Read an instance of the RSSFeed, if found.'''
        if not self.exists():
            self.create()
        rss_feed = RSSFeed("", "", "")
        feed = RSSFeed.load(rss_file)
        if not feed:
            return None
        return feed

    
    
    