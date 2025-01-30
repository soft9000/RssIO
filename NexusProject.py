#!/usr/bin/env python3
# NexusProject.py: Manage a site's RSS feed, templates, and more.
# Rev 0.04
# Status: R&D.


# 2025/01/24: Created + shared at https://github.com/soft9000/RssIO
import os
import shutil
from RssIO import *
from RssNexus import *
from Content import ContentFile
from SecIO import Enigma

class RssSite:
    ''' An RssSite is designed to read any single `input` folder, skin the text using any input-defined 
    `template` file, then place the results into a single `output` folder. Security parameters enable 
    several built-in content protection options.
    
    Ready to upload to your site, the `output` folder will also contain the `nexus.rss` file.

    A default template is provided. Feel free to change it and / or create your own template file(s) 
    to use from within your `input` file.


    Enjoy,

    Randall Nagy
    
    '''
    PREFIX = '[HTML prefix usually here - braces not required.]'
    SUFFIX = '[HTML suffix usually here - braces not required.]'
    
    RSS_NODE = FileTypes.DEFAULT_FILE_RSS

    def __init__(self, root_folder, site_url):
        if not site_url:
            site_url = 'https://www.myzite9000.com'
        if not root_folder:
            root_folder = site_url.split('/')[-1:][0]
        self.home_dir = root_folder
        sec = Enigma() # default encoding
        self.url = sec.assign(site_url)
        self.rss_file = FileTypes.home(self.home_dir, RssSite.RSS_NODE)
        nexus_folder = NexusFolder()
        nexus_folder.assign(FileTypes.home(root_folder, 'input'), FileTypes.home(root_folder, 'output'), FileTypes.home(root_folder, 'templates'))
        default_template = FileTypes.home(nexus_folder.template_dir, FileTypes.DEFAULT_FILE_TEMPLATE)
        self.nexus = RSSNexus(nexus_folder, RssTemplateFile(default_template))

    def create_input_file(self, node)->str:
        '''Create + place a node into the input folder. Content default and file suffix assured. '''
        if not node or not self.exists():
            return None
        if node.find(FileTypes.SEP) != -1:
            node = node.split(FileTypes.SEP)[:-1]
        if not node.endswith(FileTypes.FT_IN):
            node += FileTypes.FT_IN
        cf = ContentFile(FileTypes.home(self.nexus.nexus_folders.in_dir, node))
        # Add as much meta as possible:
        meta = ContentFile.DEFAULTS
        core = node.replace(FileTypes.FT_IN,'')
        meta['link'] = FileTypes.home(self.url, core + FileTypes.FT_OUT)
        if not cf.write_json(meta):
            return None
        return cf.filename

    def rmtree(self):
        ''' Safely remove sub + project folders. Return true if / when there are none. '''
        if not self.exists():
            return True
        if not self.nexus.rmtree():
            return False
        try:
            readme = FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_README)
            if os.path.exists(readme):
                os.remove(readme)
            if len(os.listdir(self.home_dir)) == 0:
                shutil.rmtree(self.home_dir)
            return not self.exists()
        except:
            pass
        return False

    def exists(self)->bool:
        ''' See if the folders exist. '''
        if not os.path.exists(self.home_dir): 
            return False
        return self.nexus.exists()
    
    def create(self)->bool:
        '''Assert site folders, default template, and a default RSS feed.'''
        if not os.path.exists(self.home_dir): 
            os.mkdir(self.home_dir)                         # create root folder
        if not self.nexus.exists():
            if not self.nexus.nexus_folders.create_folders(self.home_dir): # create input, output, and template folders
                return False
        if not self.nexus.template.exists():                # create default template file
            if not self.nexus.template.create_template_file(RssSite.PREFIX, RssSite.SUFFIX):
                return False
        zurl = FileTypes.home(self.url, RssSite.RSS_NODE)
        rss_feed = RSSFeed("Channel / Site Title", "Description of this RSS channel or site", zurl)
        if not self.exists():
            if not RSSFeed.save(rss_feed, FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_RSS)): # create the default RSS Channel
                return False
        # Final - README, info.
        readme = FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_README)
        with open(readme, 'w') as fh:
            fh.write(RssSite.__doc__)
            fh.write('Security protocols include:\n')
            for key in Enigma.protocols:
                dev = 'unsupported' if Enigma.Sec[key][2] == None else 'supported'
                fh.write(f"\t{key:^10} is presently {dev}.\n")
        return os.path.exists(readme)
    
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
    print(f"***** Testing Module {__name__}.")
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
    rss_file = FileTypes.home(site.nexus.nexus_folders.out_dir, FileTypes.DEFAULT_FILE_RSS)
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
    for ss,line in enumerate(rss_str.split('\n'),1):
        bare = line.strip()
        if  _str.find(bare) == -1:
            raise RssException(f'Line generation error {ss}: {bare}')

    # STEP: Basic content creation
    for node in 'foo', 'foo' + FileTypes.FT_IN:
        cfile = site.create_input_file(node)
        if not cfile or not os.path.exists(cfile):
            raise RssException("Content creation failure.")
        
        if not cfile.endswith(FileTypes.FT_IN):
            raise RssException("Invaild input file type assigned.")
        
        if not debug:
            os.remove(cfile)
            if os.path.exists(cfile):
                raise RssException(f'Unable to remove {cfile}.')
    
    # STEP: Complex content creations
    
    # STEP: Remove Test Site / Reset Test Case
    if not debug and not site.rmtree():
        raise RssException("Regression: Unable to remove test site.")
    print("\nTesting Success.")


if __name__ == '__main__':
    test_cases()
    
    
    