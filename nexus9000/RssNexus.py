#!/usr/bin/env python3
# RSSNexus.py: An multi-template RSS content skinner + static feed burner.
# Rev 0.05
# Status: Work in progress.

# 2025/01/23: Created + shared at https://github.com/soft9000/RssIO
# 2025/01/24: Switched to using JSON for content.

# Mission is to create the skinning + rss sharing of a static
# web feed. Input is a folder full of content. Output is a folder
# full of "skinned" content. Template folder has the file-names
# of the "skins" used to wrap each input-file.
#
# Any legacy .rss feed detected in the input-folder will be used to
# create the final output-file feed.

import os
import os.path
import shutil
from Files import *
from RssItemSecured import RSSItemSecured
from SecIO import Enigma
from RssIO import RSSFeed
from Content import ContentFile, ContentFolder
from RssTemplate import RssTemplateFile

class NexusFile:
    FILE_TYPE = FileTypes.FT_OUT

    def __init__(self, content_file:str):
        ''' Create a NexusFile with a template. NexusFile will not be ready until the
        RSSItem is_robust, which it ain't when we're first initialized. '''
        self.content_file = content_file
        self._template = RssTemplateFile(FileTypes.DEFAULT_FILE_TEMPLATE)
        self._rss_item = RSSItemSecured(ContentFile.JSON_FIELD_SET)
    
    def get_content(self) -> str:
        ''' Load / reload the JSON content file. '''
        try:
            content = ContentFile(self.content_file)
            data = content.read_json()
            if not data:
                return None
            self._rss_item = RSSItemSecured(data) 
            if not data['template'] == FileTypes.DEFAULT_FILE_TEMPLATE:
                self._template = RssTemplateFile(data['template'])
            return data['text']           
        except:
            pass
        return None

    def get_item(self)->RSSItemSecured:
        ''' Get the RSS item. '''
        return self._rss_item

    def set_item(self, title, description, link, ctime=None)->bool:
        ''' Set the RSS item assigning the title, description, 
        link. The last node of the link (document name) is used to 
        generate the file name for any NexusFile. ''' 
        for foo in title, description, link:
            if not foo:
                return False
        self._rss_item.title = title
        self._rss_item.description = description
        self._rss_item.link = link
        if ctime:
            self._rss_item.try_pubDate(ctime)
        return True

    def is_ready(self) -> bool:
        '''Make sure that the file content and the RSS / static meta is robust.'''
        if not self.get_content() or not self._rss_item:
            return False
        return self._rss_item.is_robust()
    
    def get_output_file(self, out_dir, suffix=FILE_TYPE) -> str:
        '''Qualify + test the creation of the output file in the `out_dir`.'''
        if not out_dir:
            return None
        if out_dir.endswith(suffix):
            out_dir = FileTypes.pop(out_dir)
        if not self.is_ready() or not out_dir or not os.path.exists(out_dir):
            return None
        try:
            out_file = out_dir.strip()
            if not out_file.endswith(FileTypes.SEP):
                out_file += FileTypes.SEP
            node = out_file + self._rss_item.link
            if not node.find(FileTypes.SEP) == -1:
                node = out_file + self._rss_item.link.split(FileTypes.SEP)[-1]
            if not node.endswith(suffix):
                node += suffix
            if os.path.exists(node):
                return node
            with open(node, 'w') as fh:
                fh.write('test_write')
            os.unlink(node)
            return node
        except:
            return None

    def presto(self, template_file:RssTemplateFile, data:str) -> str:
        '''Read the template with template. Secure iff applied.'''
        if not self.is_ready():
            return None
        sec = Enigma(self._rss_item.json['security'])
        if sec is not None:
            content = template_file.merge_with(sec.en(data))
        else:
            content = template_file.merge_with(data)           
        if not content:
            return None
        return content
    
    def create_output(self, template_file:RssTemplateFile, out_dir) -> bool:
        ''' Merge the data with the template so as to create z output file. '''
        content = self.presto(template_file, self.get_content())
        if not content:
            return False
        try:
            ofile =  self.get_output_file(out_dir)
            if not ofile:
                return False
            with open(ofile, 'w') as fh:
                fh.write(content)
            return True
        except Exception as e:
            print(e)
            return False

class NexusFolders:
    ''' Nexus of folders for RSS to manage. Put content in the input folder, templates in 
    the template folder, and ye olde 'skinned' content + the RSS meta will be placed in 
    the output folder. The only thing to do would be to upload the generated output folder 
    to the same-named bucket / folder on your web server. '''

    def __init__(self):
        ''' Create an empty (is_null()) Nexus. '''
        self.in_dir = self.out_dir = self.template_dir = None

    def assign(self, in_dir, out_dir, template_dir) -> bool:
        ''' Nexus folders do NOT need to exist before being assigned. '''
        for foo in in_dir, out_dir, template_dir:
            if not foo:
                return False
        self.in_dir = in_dir 
        self.out_dir = out_dir
        self.template_dir = template_dir
        return True
    
    def makedirs(self) -> bool:
        ''' Create the folders if they don't exist. '''
        for foo in self.in_dir, self.out_dir, self.template_dir:
            if not os.path.exists(foo):
                try:
                    os.makedirs(foo)
                except:
                    return False
        return True
    
    def rmtree(self) -> bool:
        ''' Remove the folders. '''
        for foo in self.in_dir, self.out_dir, self.template_dir:
            if os.path.exists(foo):
                try:
                    shutil.rmtree(foo)
                except:
                    return False
        return True
    
    def create_folders(self, root_dir:str) -> bool:
        ''' Create the Nexus folders. '''
        if not root_dir:
            return False
        for foo in self.in_dir, self.out_dir, self.template_dir:
            if not foo:
                return False
            if not os.path.exists(foo):
                try:
                    os.makedirs(foo)
                except:
                    return False
        return True
    
    def exists(self) -> bool:
        ''' Make sure that the folders exist. '''
        if self.is_null():
            return False
        for foo in self.in_dir, self.out_dir, self.template_dir:
            if not os.path.exists(foo) or not os.path.isdir(foo):
                return False
        return True
    
    def is_null(self) -> bool:
        ''' See if we've assigned all Nexus folders. Folders need NOT exist.'''
        for foo in self.in_dir, self.out_dir, self.template_dir:
            if not foo:
                return True
        return False
    
    def into_root(self, file_name:str) -> str:
        ''' Get the fully qualified file name for the parent folder. '''
        if not file_name or self.is_null():
            return None
        if self.out_dir.find(FileTypes.SEP) == -1:
            return './' + file_name     # root is best 
        nodes = self.out_dir.split(FileTypes.SEP)
        nodes = nodes[:-1]
        nodes.append(file_name)
        return './' + FileTypes.SEP.join(nodes)    # parent is best


from RssItemMeta import RSSItemMeta
from RssExceptions import RssException
class RSSNexus:
    ''' The RSSNexus is the heart of any RSS feed generator. An RSSNexus's content root is the 
    channel's rss file. Unlike the RSSSite the content of an RSSNexus might be anywhere. '''
    def __init__(self, project:NexusFolders, template:RssTemplateFile):
        self.nexus_folders = project
        self.input_files = []
        self.template = template
        self.rss_channel = None
    
    def rmtree(self)->bool:
        ''' Remove the nexus - True if removed. '''
        if self.exists():
            return self.nexus_folders.rmtree()
        return True
    
    def exists(self)->bool:
        ''' See if the Nexus folders exist. '''
        return self.nexus_folders.exists()
    
    def set_meta(self, rss_feed:RSSItemMeta)->bool:
        '''Copy-in the metadata (isa RSSFeed!) that this channel Nexus will use - no items, please.'''
        if rss_feed and rss_feed.is_robust():
            self.rss_channel = rss_feed
            return True
        else:
            return False
    
    def item_count(self)->int:
        '''Return the number of  items in the feed.'''
        if self.input_files:
            return len(self.input_files)
        return 0
    
    def add_item(self, nexus_file:NexusFile)->bool:
        '''Safe-assign / append a NexusFile. '''
        if nexus_file and nexus_file.is_ready():
            self.input_files.append(nexus_file)
            return True
        return False

    def validate(self):
        ''' Raise an exception if this Nexus is not valid. '''
        if not self.rss_channel or not self.rss_channel.is_robust():
            raise RssException("Error 001: Channel metadata has not been assigned to this Nexus.")
        if not self.nexus_folders or self.nexus_folders.is_null():
            raise RssException("Error 002: Nexus project has not been assigned.")
        if not self.template or not self.template.exists():
            raise RssException("Error 003: Nexus is not valid.")
        for ss, item in enumerate(self.input_files):
            if not item or not item.is_ready():
                raise RssException(f'Error 004: RSS Item {ss} is not robust.')
        return True

    def generate(self, web_root_url, protect=True) -> bool:
        ''' Generate the RSS feed and static site. Raises an RssException on error. '''
        self.validate()
        rss_feed = RSSFeed()
        rss_feed.assign(self.rss_channel.title, self.rss_channel.description, self.rss_channel.link, self.rss_channel.pubDate, self.rss_channel.keywords)
        for ss, input_file in enumerate(self.input_files):
            out_dir = self.nexus_folders.out_dir
            out_file = input_file.content_file.replace(FileTypes.FT_IN,FileTypes.FT_OUT) # change type
            opos = out_file.find(self.nexus_folders.in_dir)
            if not opos == -1: 
                # transition from input to output location:
                opos = opos + len(self.nexus_folders.in_dir)
                rval = out_file[opos:]
                out_dir = FileTypes.home(out_dir, FileTypes.pop(rval))  # output folder
                ndir = ContentFolder(out_dir)
                # make sure the output location is ready
                if not ndir.exists() and not ndir.create():
                    return False
            if not input_file.create_output(self.template, out_dir):
                return False
            zitem = input_file.get_item()
            # Update the RSS link:
            zitem.link = FileTypes.home(web_root_url,rval)
            if protect and zitem.json:
                cry = Enigma(zitem.json['security'])
                zitem.link = cry.assign(zitem.link)
            rss_feed.add_item(zitem)

        home_rss      = FileTypes.home(self.nexus_folders.out_dir, FileTypes.DEFAULT_FILE_RSS)
        rss_feed.link = FileTypes.home(web_root_url,         FileTypes.DEFAULT_FILE_RSS)

        if not RSSFeed.write_rss(rss_feed, home_rss):
            return False
        return True

def test_cases(debug=False):
    print(f"***** Testing Module {__name__}.")
    web_site = 'https://www.soft9000.com'

    # STEP: SETUP NEXUS FOLDERS
    nexus_folders = NexusFolders()
    if not nexus_folders.assign('test_in', 'test_out', 'test_template'):
        raise RssException('Error: Unable to assign Nexus folders.')
    if not nexus_folders.makedirs():
        raise RssException('Error: Unable to create Nexus folders.')
    
    # STEP: TEST TEMPLATE FILE MERGE
    test_template = RssTemplateFile(FileTypes.home(nexus_folders.template_dir, 'test_template' + FileTypes.FT_TEMPLATE))
    if not test_template.create_template_file('Hello, ', '!'):
        raise RssException('Error: Unable to create template file.')
    content = test_template.merge_with('World')
    if not content  == 'Hello, World!':
        raise RssException('Error: Unable to merge template file.')

    rss_feed= RSSFeed()
    rss_feed.title = "Testing Success"
    rss_feed.description = "A feed test for the manual creation"
    rss_feed.link = "./test_out/index.rss"
    rss_nexus = RSSNexus(nexus_folders, test_template)
        
    # STEP: TEST FILE MULI-FILE CONTENT FILE CREATIONS (NO RSS)
    for content in "fred", "ralph", "joe":
        znode = content + FileTypes.FT_IN
        content_file_name_in = FileTypes.home(nexus_folders.in_dir, znode)
        # Save the data structure into content file:
        create_json = ContentFile(content_file_name_in)
        jdata = ContentFile.JSON_FIELD_SET
        jdata['text'] = content
        jdata['link'] = FileTypes.home(web_site, FileTypes.home(nexus_folders.out_dir, content + FileTypes.FT_OUT))
        if not create_json.write_json(jdata):
            raise RssException(f'Unable to create "{create_json.filename}"')
        # Create the NexusFile for the RSS feed:
        nexus_file = NexusFile(content_file_name_in)
        if not nexus_file.set_item('zTitle for ' + content, 'zDescr for ' + content, jdata['link']):
            raise RssException('Error: Unable to set RSS item.')
        if not nexus_file.create_output(test_template, nexus_folders.out_dir):
            raise RssException('Error: Unable to create RSS output.')
        # Keep it.
        rss_feed.add_item(nexus_file.get_item()) # for the next test
        rss_nexus.add_item(nexus_file)

    # STEP: TEST MANUAL RSSFeed CREATION
    RSSFeed.write_rss(rss_feed, FileTypes.home(nexus_folders.out_dir, "test_index.rss"))

    # STEP: TEST THE RSSFolder AUTO (mega?) GENERATOR
    rss_nexus.set_meta(rss_feed)
    rss_nexus.generate(web_site)

    funko = RSSNexus(nexus_folders, test_template)
    ref = funko.nexus_folders.out_dir 
    funko.nexus_folders.out_dir = 'a/b/c'
    foo = funko.nexus_folders.into_root('index.rss')
    if foo != './a/b/index.rss':
        raise RssException('Error: Unable to create parented home_out.')
    funko.nexus_folders.out_dir = 'a'
    foo = funko.nexus_folders.into_root('index.rss')
    if foo != './index.rss':
        raise RssException('Error: Unable to create rooted home_out.')
    funko.nexus_folders.out_dir = ref
    
    # STEP: TEST RSSNexus CONTENT DETECTION

    # STEP: TEST RSS UPDATE
    
    # STEP: VERIFY RSSNexus FILE SKINNING
    
    # STEP: POST-TEST CLEANUP
    if not debug and not rss_nexus.rmtree():
        raise RssException('Error: Unable to remove Nexus test folders.')

    print('Testing Success.')


if __name__ == '__main__':
    test_cases()