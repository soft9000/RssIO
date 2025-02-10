#!/usr/bin/env python3
# Content.py: An multi=template RSS content skinner + static feed burner.
# Rev 0.02
# Status: Testing Success.

# 2025/01/25: Created + shared at https://github.com/soft9000/RssIO

import os.path
import json, time
from Files import *
from RssTemplate import RssTemplateFile
from RssExceptions import RssException

class ContentFile:

    FILE_TYPE = FileTypes.FT_IN                          # Default file type for content files.
    DEFAULT_TEMPLATE = FileTypes.DEFAULT_FILE_TEMPLATE   # NOT the FILE_TYPE!
    ALL_PROJECTS = './'                                  # Location where RSS all projects should go.

    JSON_FIELD_SET = {
        "title": "Sample Title",
        "description": "Sample Description",
        "template": DEFAULT_TEMPLATE,
        "pubDate": time.ctime(),
        "security": "DEFAULT",
        "link": '',
        "text": "Sample text content."
    }

    def __init__(self, filename):
        self.filename = filename

    def fixup(self, data):
        for key in ContentFile.JSON_FIELD_SET:
            if key not in data:
                data[key] = ContentFile.JSON_FIELD_SET[key]
        return None # meh

    def read_json(self)->dict:
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.fixup(data)
                return data
        except FileNotFoundError:
            raise RssException(f"File {self.filename} not found.")

        except json.JSONDecodeError:
            raise RssException(f"Error decoding JSON from file {self.filename}.")
    
    def is_current(self, jdict)->bool:
        '''Verify dictionary has all of the present keys.'''
        if not jdict:
            return False
        for key in ContentFile.JSON_FIELD_SET:
            if not key in jdict:
                return False
        return True
    
    def exists(self):
        '''See if the file is on the file system.'''
        return os.path.exists(self.filename)

    def write_json(self, data)->bool:
        '''Save the data to the file name. True if file was created. '''
        if not isinstance(data, dict):
            raise RssException("Data must be a dictionary.")

        required_fields = {"title", "description", "text"}
        if not required_fields.issubset(data.keys()):
            raise RssException(f"Data must contain the following fields: {required_fields}")

        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            raise RssException(f"Error writing to file {self.filename}: {e}")
        
        return self.exists()


def test_cases(debug=False):
    import os
    print(f"***** Testing Module {__name__}.")
    for afile in '~example', '~example'+ ContentFile.FILE_TYPE:
        file_handler = ContentFile(afile)
        
        if not file_handler.write_json(ContentFile.JSON_FIELD_SET):
            raise RssException(f'Unable to create content for {afile}')
        
        if not file_handler.exists():
            raise RssException(f'Failed to create content for {afile}')
        
        data_read = file_handler.read_json()
        if data_read:
            if not file_handler.is_current(data_read):
                raise RssException("Invalid tag set loaded.")
            if debug:
                print(data_read)
            else:
                os.unlink(afile)
                if file_handler.exists():
                    raise RssException(f'Failed to REMOVE {afile}')
            print("Testing Success.")
        
        else:
            raise RssException("Error: Cannot read test json file.")
    

if __name__ == "__main__":
    test_cases()