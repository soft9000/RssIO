#! /usr/bin/env python3
#!/usr/bin/env python3
# NexusProject.py: Manage a site's RSS feed, templates, and more.
# Rev 0.02
# Status: R&D.

# 2025/01/24: Created + shared at https://github.com/soft9000/RssIO
from RssIO import *
from RssNexus import *
from Content import ContentFile

class RssSite:
    PREFIX = '[HTML prefix usually here - braces not required.]'
    SUFFIX = '[HTML suffix usually here - braces not required.]'
    
    RSS_NODE = FileTypes.DEFAULT_FILE_RSS

    def __init__(self, root_folder, site_url):
        self.home_dir = root_folder
        self.url = site_url
        self.rss_file = FileTypes.home(self.home_dir, RssSite.RSS_NODE)
        nexus_folder = NexusFolder()
        nexus_folder.assign(FileTypes.home(root_folder, 'input'), FileTypes.home(root_folder, 'output'), FileTypes.home(root_folder, 'templates'))
        default_template = FileTypes.home(nexus_folder.template_dir, FileTypes.DEFAULT_FILE_TEMPLATE)
        self.nexus = RSSNexus(nexus_folder, RssTemplateFile(default_template))

    def exists(self)->bool:
        if not os.path.exists(self.home_dir): 
            return False
        return self.nexus.exists()
    
    def create(self)->bool:
        '''Assert site folders, default template, and a default RSS feed.'''
        if not os.path.exists(self.home_dir): 
            os.mkdir(self.home_dir)                         # create root folder
        if not self.nexus.exists():
            if not self.nexus.folders.create_folders(self.home_dir): # create input, output, and template folders
                return False
        if not self.nexus.template.exists():                # create default template file
            if not self.nexus.template.create_template_file(RssSite.PREFIX, RssSite.SUFFIX):
                return False
        zurl = FileTypes.home(self.url, RssSite.RSS_NODE)
        rss_feed = RSSFeed("Channel / Site Title", "Description of this RSS channel or site", zurl)
        if not self.exists():
            if not RSSFeed.save(rss_feed, FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_RSS)): # create the default RSS Channel
                return False
        return True
    
    def update(self)->bool:
        '''Update the RSS feed.'''
        feed = RssSite.read_feed(self.rss_file)
        if not feed:
            return False
        self.nexus.nexus_files.clear()
        for file in os.listdir(self.nexus.input_dir):
            if file.endswith(ContentFile.FILE_TYPE):
                # STEP: Get the meta from the topic / json file.
                node = FileTypes.home(self.nexus.input_dir, file)
                topic = ContentFile(node)
                if not topic.read_json():
                    continue
                item = RSSItem(topic.title, topic.description, topic.url, topic.date)
                feed.add_item(item)
                self.nexus.add_item(NexusFile(node))

        # STEP: Merge the template with the input topic.
        if not self.nexus.generate(self.url, True):
            raise RssException("Error 305: Unable to generate nexus content.")
        # STEP: Update the RSS folder to refer to the newly merged output.
        return RSSFeed.save(feed)

    def read_feed(self, rss_file:str)->RSSFeed:
        '''Read an instance of the RSSFeed, if found.'''
        return RSSFeed.load(rss_file)
    
def test_cases(debug=False):
    # STEP: Default Site Creation + Load + Existance
    tsite = './Test001'
    rss_str = """<?xml version="1.0" ?>
<rss version="2.0">   
  <channel>
    <title>Channel / Site Title</title>
    <link>https://www.soft9000.com/nexus.rss</link>
    <description>Description of this RSS channel or site</description>
    <generator>https://github.com/soft9000/RssIO</generator>
  </channel>
</rss>"""
    site = RssSite(tsite,"https://www.soft9000.com")
    rss_file = FileTypes.home(site.nexus.folders.out_dir, FileTypes.DEFAULT_FILE_RSS)
    if not site.create():
        raise RssException('Site creation failure.')
    with open(rss_file, 'w') as fh:
        fh.write(rss_str)
    feed = site.read_feed(rss_file)
    if not feed:
        raise RssException(f'Unable to RssSite.read_feed({tsite}).')
    
    if not site.exists():
        raise RssException("RssSite.exists() failure.")

    # STEP: Regression detection / string Comp
    _str = feed.to_string()
    for ss,line in enumerate(rss_str.split(),1):
        if  line.strip().find(line):
            raise RssException(f'Line generation error {ss}')

    # STEP: Basic content creation
    # STEP: Complex content creations
    print("\nTesting Success.")
    # TODO: Remove Test Site / Reset Test Case


if __name__ == '__main__':
    test_cases()
    
    
    