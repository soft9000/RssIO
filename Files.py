'''Common File 'Meta. Some day to be properties when externalized.'''

class FileTypes:
    SEP = '/'
    FT_OUT = '.html' # NexusFile.FILE_TYPE
    FT_TEMPLATE  = '.txt'  # RssTemplateFile.FILE_TYPE
    FT_IN = '.json' # ContentFile.FILE_TYPE
    DEFAULT_FILE_RSS   = 'nexus.rss'
    DEFAULT_FILE_TEMPLATE = "default" + FT_TEMPLATE

    @staticmethod
    def home(path:str, node:str, sep=SEP)->str:
        ''' Reliably place a node into a parent folder. Test case is a good demo.'''
        if not path:
            path = ''
        if not node:
            node = ''
        while node and node.startswith(sep):
            node = node[1:]
        while path and path.endswith(sep):
            path = path[:-1]
        if path.endswith(sep):
            return path + node
        return path + sep + node

if __name__ == '__main__':
    foo = FileTypes.home(None,None)
    if foo != '/':
        raise Exception(f"Regression 00100: FileTypes.home() should be None, got '{foo}'.")
    
    foo = FileTypes.home('zoom',None)
    if foo != 'zoom/':
        raise Exception(f"Regression 00110: FileTypes.home() should be None, got '{foo}'.")
    
    foo = FileTypes.home('zoom','bat')
    if foo != 'zoom/bat':
        raise Exception(f"Regression 00120: FileTypes.home() should be None, got '{foo}'.")
    
    foo = FileTypes.home('/////zoom','bat/////')
    if foo != '/////zoom/bat/////':
        raise Exception(f"Regression 00130: FileTypes.home() should be None, got '{foo}'.")
    
    foo = FileTypes.home('zoom/////','/////bat')
    if foo != 'zoom/bat':
        raise Exception(f"Regression 00140: FileTypes.home() should be None, got '{foo}'.")

    print("Testing Success.")    