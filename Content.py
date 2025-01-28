#!/usr/bin/env python3
# TopicTemplate.py: An multi=template RSS content skinner + static feed burner.
# Rev 0.02
# Status: Lightly tested.

# 2025/01/25: Created + shared at https://github.com/soft9000/RssIO

import json, time
from Files import *
from RssTemplate import RssTemplateFile
from RssExceptions import RssException

class ContentFile:

    FILE_TYPE = FileTypes.FT_IN
    DEFAULT_TEMPLATE = FileTypes.DEFAULT_FILE_TEMPLATE   # NOT the FILE_TYPE!

    DEFAULTS = {
        "title": "Sample Title",
        "description": "Sample Description",
        "template": DEFAULT_TEMPLATE,
        "pubDate": time.ctime(),
        "link": '',
        "text": "Sample text content."
    }

    def __init__(self, filedata):
        self.filedata = filedata

    def fixup(self, data):
        for key in ContentFile.DEFAULTS:
            if key not in data:
                data[key] = ContentFile.DEFAULTS[key]
        return None # meh

    def read_json(self)->dict:
        try:
            with open(self.filedata, 'r') as file:
                data = json.load(file)
                self.fixup(data)
                return data
        except FileNotFoundError:
            raise RssException(f"File {self.filedata} not found.")

        except json.JSONDecodeError:
            raise RssException(f"Error decoding JSON from file {self.filedata}.")

    def write_json(self, data):
        if not isinstance(data, dict):
            raise RssException("Data must be a dictionary.")
            return

        required_fields = {"title", "description", "text"}
        if not required_fields.issubset(data.keys()):
            raise RssException(f"Data must contain the following fields: {required_fields}")
            return

        try:
            with open(self.filedata, 'w') as file:
                json.dump(data, file, indent=4)
                return True
        except IOError as e:
            raise RssException(f"Error writing to file {self.filedata}: {e}")


if __name__ == "__main__":
    import os
    afile = '~example'+ ContentFile.FILE_TYPE
    file_handler = ContentFile(afile)
    
    file_handler.write_json(ContentFile.DEFAULTS)
    
    data_read = file_handler.read_json()
    if data_read:
        print(data_read)
        print("Testing Success.")
        os.unlink(afile)
    else:
        print("Error: Cannot read test json file.")