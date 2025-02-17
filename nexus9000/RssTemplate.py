#!/usr/bin/env python3
# RssTemplate.py: Minimalist template file support.
# Rev 0.02
# Status: Lightly tested.

import os, os.path
from Files import *

class RssTemplateFile:
    
    TEMPLATE_TOKEN = '.$NojRssIOTok$.'

    FILE_TYPE = FileTypes.FT_TEMPLATE
    
    def __init__(self, template_file_name, template_token = TEMPLATE_TOKEN):
        self.filename = template_file_name
        self.token = template_token
    
    @staticmethod
    def parse(filename:str, token:str=TEMPLATE_TOKEN)->str|None:
        '''Instantiate a template from an external template file.'''
        try:
            if filename and os.path.exists(filename):
                result = RssTemplateFile(filename, token)
                if result.read_template_file():
                    return result
        except:
            pass
        return None
        
    
    def exists(self)->bool:
        '''See if the template file name esists. '''
        try:
            if self.filename:
                return os.path.exists(self.filename)
        except:
            pass
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
    
    def read_template_file(self)->str|None:
        '''Read the template file. WYSIWYG'''
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except:
            return None

    def merge_with(self, data:str)->str|None:
        '''Merge the data with the template by reading + replacing the 
        token with the data.'''
        try:
            with open(self.filename, 'r') as file:
                return file.read().replace(self.token, data)
        except:
            return None



