#!/usr/bin/env python3
# Nexus.py: Manage a site's RSS feed, templates, and more.
# Rev 0.06
# Status: R&D.

# 2025/01/24: Created + shared at https://github.com/soft9000/RssIO

import os
import shutil
from RssIO import *
from RssNexus import *
from Content import ContentFile
from SecIO import Enigma
from UrlIO import UrlParser
        

class RSSSite:
    '''An RssSite is designed to read any single `input` folder, skin the text using any input-defined 
    `template` file, then place the results into a single `output` folder. Security parameters enable 
    several built-in content protection options.
    
    Ready to upload to your site, the content within that `output` folder will also contain your final 
    `nexus.rss` file. Everything underneath `output` is designed to work directly underneath any web's 
    "root" location.
    
    NOTES:
    -----
    (1) A default document template / content skinner is provided. Feel free to change it and / or create 
    your own template file(s) to use from within your `input` file(s.)
    
    (2) The default security is clear-text. Anyone waneeding (want + needing =) additional security should 
    update either this code or use one of the no-risk encodings, below. THIS PROJECT IS INTENDED FOR USE 
    WITH PUBLIC SECURITY PROTOCOLS, ONLY. BE SURE TO UNDERSTAND THE RISK OF PRIVATELY PROTECTING YOUR CONTENT 
    FROM GOVERNMENTAL EYES. DON'T DO ANYTHING THAT WILL LAND YOU IN PRISON!

    Enjoy,

    Randall Nagy
    https://ko-fi.com/randallnagy
    
    '''
    PREFIX = '''<!DOCTYPE html><head><title>soft9000/RssIO: A SECURABLE way to read, write, and manage as many Really Simply Syndications as possible.</title></head><html><body>'''
    SUFFIX = '</body></html>'
    
    RSS_NODE = FileTypes.DEFAULT_FILE_RSS

    def __init__(self, root_folder, site_url):
        if not site_url:
            site_url = 'https://www.myzite9000.com'
        if not root_folder:
            root_folder = site_url.split('/')[-1:][0]
        if not root_folder:
            root_folder = site_url
        _dict = UrlParser.parse(root_folder)
        if _dict['site'] is not None:
                root_folder = FileTypes.detox(ContentFile.ALL_PROJECTS) + '/' + _dict['site']
        self.home_dir = root_folder
        self.url = site_url
        self.rss_file = FileTypes.home(self.home_dir, RSSSite.RSS_NODE)
        nexus_folder = NexusFolder()
        nexus_folder.assign(FileTypes.home(root_folder, 'input'), FileTypes.home(root_folder, 'output'), FileTypes.home(root_folder, 'templates'))
        default_template = FileTypes.home(nexus_folder.template_dir, FileTypes.DEFAULT_FILE_TEMPLATE)
        self.nexus = RSSNexus(nexus_folder, RssTemplateFile(default_template))
    
    @staticmethod
    def equals(a, b)->bool:
        '''See if the folders are the same.'''
        if a and b:
            return a.home_dir == b.home_dir
        return False
    
    def add_item(self, item:NexusFile)->bool:
        '''Add a NexusFile to the RSSSite.'''
        if isinstance(item, NexusFile):
            return self.nexus.add_item(item)
        return False

    def create_input_file(self, node, security=None)->str:
        '''Create + place a node into the input folder. Content default and file suffix assured. '''
        if not node or not self.folders_exist():
            return None
        if node.find(FileTypes.SEP) != -1:
            node = node.split(FileTypes.SEP)[:-1]
        if not node.endswith(FileTypes.FT_IN):
            node += FileTypes.FT_IN
        cf = ContentFile(FileTypes.home(self.nexus.nexus_folders.in_dir, node))
        # Add as much meta as possible:
        meta = ContentFile.JSON_FIELD_SET
        if security is not None:
            meta['security'] = security
        core = node.replace(FileTypes.FT_IN,'')
        meta['link'] = FileTypes.home(self.url, core + FileTypes.FT_OUT)
        if not cf.write_json(meta):
            return None
        return cf.filename

    def rmtree(self):
        ''' Safely remove sub + project folders. Return true if / when there are none. '''
        if not self.folders_exist():
            return True
        if not self.nexus.rmtree():
            return False
        try:
            readme = FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_README)
            if os.path.exists(readme):
                os.remove(readme)
            if len(os.listdir(self.home_dir)) == 0:
                shutil.rmtree(self.home_dir)
            return not self.folders_exist()
        except:
            pass
        return False
    
    def remove_rss_file(self)->bool:
        '''Remove the RSS file, only. Returns True or an OS Exception ff the RSS files cannot be deleted.'''
        if self.rss_file and os.path.exists(self.rss_file):
            os.remove(self.rss_file) # exception ok here.
        return True

    def folders_exist(self)->bool:
        ''' See if the folders exist. '''
        if not os.path.exists(self.home_dir): 
            return False
        return self.nexus.exists()
    
    @staticmethod
    def get_content_file(filename:str)->ContentFile:
        '''Concoct + return a ContentFile from a qualified fine-name.'''
        from Content import ContentFile
        topic = ContentFile(filename)
        if not topic.read_json():
            return None
        return topic

    @staticmethod
    def load_item(filename:str)->RSSItemSecured:
        '''Read the JSON from a qualified file-name.'''
        topic = RSSSite.get_content_file(filename)
        if topic:
            json = topic.read_json()
            if not json:
                return None
            item = RSSItemSecured(json)
            return item
        return None
    
    def rss_replace(self, rss_str)->bool:
        '''Overwrite the default rss file with whatever the user needs.'''
        if not rss_str:
            rss_str = ''
        with open(self.rss_file, 'w') as fh:
            fh.write(rss_str)
        return os.path.exists(self.rss_file)
    
    def setup(self)->bool:
        '''Create a default set of site folders, a default template, as well as a default RSS feed.'''
        if not os.path.exists(self.home_dir): 
            os.mkdir(self.home_dir)                         # create root folder
        self.rss_file = FileTypes.home(self.nexus.nexus_folders.out_dir, FileTypes.DEFAULT_FILE_RSS)   
        if not self.nexus.exists():
            if not self.nexus.nexus_folders.create_folders(self.home_dir): # create input, output, and template folders
                return False
        if not self.nexus.template.exists():                # create default template file
            if not self.nexus.template.create_template_file(RSSSite.PREFIX, RSSSite.SUFFIX):
                return False
        zurl = FileTypes.home(self.url, RSSSite.RSS_NODE)
        rss_feed = RSSFeed()
        rss_feed.assign("Channel / Site Title", "Description of this RSS channel or site", zurl)
        if not self.folders_exist():
            if not RSSFeed.write_rss(rss_feed, FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_RSS)): # create the default RSS Channel
                return False
        # Final - README, info.
        readme = FileTypes.home(self.home_dir, FileTypes.DEFAULT_FILE_README)
        with open(readme, 'w') as fh:
            fh.write(RSSSite.__doc__)
            fh.write('Security protocols include:\n')
            for key in Enigma.PROTOCOL_KEYS:
                dev = 'unsupported' if Enigma.PROTOCOL_DATA[key][2] == None else 'supported'
                fh.write(f"\t{key:^10} is presently {dev}.\n")
        return os.path.exists(readme)
    
    def generate(self)->bool:
        '''Gentere the RSS feed, as well as any final content.'''
        # STEP: Merge the template with the input topic.
        feed = self.read_feed()
        if not feed:
            return False
        if not self.nexus.generate(self.url, True):
            return False
        return True

    def reload(self)->int:
        '''Populate the feed with any input / json topical information.'''
        self.nexus.nexus_files.clear()
        for file in os.listdir(self.nexus.nexus_folders.in_dir):
            if file.endswith(ContentFile.FILE_TYPE):
                # STEP: Get the meta from the topic / json file.
                fqfilename = FileTypes.home(self.nexus.nexus_folders.in_dir, file)
                sec_item = self.load_item(fqfilename)
                if not sec_item:
                    raise RssException(f"Unable to import {fqfilename}.")
                self.nexus.add_item(NexusFile(fqfilename))  # uses common meta
        return self.nexus.item_count()

    def read_feed(self)->RSSFeed:
        '''Read an instance of the RSSFeed, if found.'''
        self.nexus.rss_channel =  RSSFeed.load(self.rss_file)
        return self.nexus.rss_channel  # none is ok
    
def test_cases(debug=False):
    print(f"***** Testing Module {__name__}.")
    # STEP: Default Site Creation + Load + Existance
    tsite = 'http://www.MySite.org'
    rss_str = """<?xml version="1.0" ?>
<rss version="2.0">   
  <channel>
    <title>Channel / Site Title</title>
    <link>https://www.soft9000.com/nexus.rss</link>
    <description>Description of this RSS channel or site</description>
    <generator>https://github.com/soft9000/RssIO</generator>
  </channel>
</rss>"""
    site = RSSSite(tsite,"https://www.soft9000.com")
    if not site.setup():
        raise RssException('Site creation failure.')
    if not site.rss_replace(rss_str):
        pass
    feed = site.read_feed()
    if not feed:
        raise RssException(f'Unable to RssSite.read_feed({tsite}).')
    
    if not site.folders_exist():
        raise RssException("RssSite.exists() failure.")

    # STEP: Regression detection / string Comp
    _str = feed.to_string()
    for ss,line in enumerate(rss_str.split('\n'),1):
        bare = line.strip()
        if  _str.find(bare) == -1:
            print(_str)
            raise RssException(f'Line detection error {ss}: {bare}')

    # STEP: Basic RSS Site UPDATE
    for node in 'foo', 'foo' + FileTypes.FT_IN:
        icfile = site.create_input_file(node)
        if not icfile or not os.path.exists(icfile):
            raise RssException("Input file creation failure 1.")
        
        if not icfile.endswith(FileTypes.FT_IN):
            raise RssException("Invaild input file type assigned 2.")
        
        os.remove(icfile)
        if os.path.exists(icfile):
            raise RssException(f'Unable to remove {icfile}.')

    # STEP: Complex content creations (secured)   
    from SecIO import Enigma
    for node in Enigma.PROTOCOL_KEYS:
        icfile = site.create_input_file(node,security=node)
        if not icfile or not os.path.exists(icfile):
            raise RssException("Input file creation failure 2.")
        
        if not icfile.endswith(FileTypes.FT_IN):
            raise RssException("Invaild input file type assigned 2.")
        
        content = ContentFile(icfile)
        jdict = content.read_json()
        if not content.is_current(jdict):
            raise RssException(f"JSON I/O Error [{jdict}], [{icfile}]")
        if not site.add_item(NexusFile(icfile)):
            raise RssException(f"Unable to add {icfile} content to {site.rss_file}.")

    if not site.generate():
        raise RssException(f"Unable to re-create {site.rss_file}")
    
    # STEP: Remove Test Site / Reset Test Case
    if not debug and not site.rmtree():
        raise RssException("Regression: Unable to remove test site.")
    print("\nTesting Success.")


if __name__ == '__main__':
    test_cases()
    
    
    