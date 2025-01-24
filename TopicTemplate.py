import json
from Files import *
from RssTemplate import RssTemplateFile
from RssExceptions import RssException

class TopicFile:

    FILE_TYPE = FileTypes.TopicFileType

    def __init__(self, filedata):
        self.filedata = filedata

    def read_json(self):
        try:
            with open(self.filedata, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            raise RssException(f"File {self.filedata} not found.")
            return None
        except json.JSONDecodeError:
            raise RssException(f"Error decoding JSON from file {self.filedata}.")
            return None

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
        except IOError as e:
            raise RssException(f"Error writing to file {self.filedata}: {e}")

if __name__ == "__main__":
    file_handler = TopicFile('~example'+ TopicFile.FILE_TYPE)
    
    # Writing to JSON file
    data_to_write = {
        "title": "Sample Title",
        "description": "Sample Description",
        "template": "default" + RssTemplateFile.FILE_TYPE,
        "pubDate": "2025-01-22",
        "text": "Sample text content."
    }
    file_handler.write_json(data_to_write)
    
    # Reading from JSON file
    data_read = file_handler.read_json()
    if data_read:
        print(data_read)