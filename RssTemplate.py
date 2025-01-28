#!/usr/bin/env python3
# RssTemplate.py: Minimalist template file support.
# Rev 0.01
# Status: Lightly tested.

import os, os.path
from Files import *

class RssTemplateFile:

    FILE_TYPE = FileTypes.FT_TEMPLATE
    
    def __init__(self, template_file_name, template_token = '.$NojRssIOTok$.'):
        self.filename = template_file_name
        self.token = template_token
    
    def exists(self):
        '''See if the template file name esists. '''
        if self.filename:
            return os.path.exists(self.filename)
        return False
    
    def create_template_file(self, prefix:str, suffix:str)->bool:
        '''Create a file by simply inserting the template token between 
        the prefix and the suffic strings.'''
        try:
            with open(self.filename, 'w') as file:
                file.write(prefix + self.token + suffix)
            return os.path.exists(self.filename)
        except:
            return False
    
    def read_template_file(self)->str:
        '''Read the template file. WYSIWYG'''
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except:
            return None

    def merge_with(self, data:str)->str:
        '''Merge the data with the template by reading + replacing the 
        token with the data.'''
        try:
            with open(self.filename, 'r') as file:
                return file.read().replace(self.token, data)
        except:
            return None



