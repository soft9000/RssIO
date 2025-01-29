'''Common File 'Meta. Some day to be properties when externalized.'''

class FileTypes:
    SEP = '/'
    FT_OUT = '.html' # NexusFile.FILE_TYPE
    FT_TEMPLATE  = '.txt'  # RssTemplateFile.FILE_TYPE
    FT_IN = '.json' # ContentFile.FILE_TYPE
    DEFAULT_FILE_RSS   = 'nexus.rss'
    DEFAULT_FILE_TEMPLATE = "default" + FT_TEMPLATE

    @staticmethod
    def detox(node:str, sep=SEP)->str:
        if not node:
            return ''
        while node and node.startswith(sep):
            node = node[1:]
        while node and node.endswith(sep):
            node = node[:-1]
        return node

    @staticmethod
    def last_name(node:str, sep=SEP)->str:
        node = FileTypes.detox(node, sep)
        if node.find(FileTypes.SEP) != -1:
            nodes = node.split(sep)
            node = nodes[-1:][0]
        return node

    @staticmethod
    def home(path:str, node:str, sep=SEP)->str:
        ''' Reliably place a node into a parent folder. Test case is a good demo.'''
        if not path:
            path = ''
        if not node:
            node = ''
        node = FileTypes.detox(node, sep)
        path = FileTypes.detox(path, sep)
        return path + sep + node


def test_cases(debug=False):
    foo = FileTypes.home(None,None)
    if foo != '/':
        raise Exception(f"Regression 00100: FileTypes.home() should be None, got '{foo}'.")
    
    foo = FileTypes.home('zoom',None)
    if foo != 'zoom/':
        raise Exception(f"Regression 00110: FileTypes.home() should be 'zoom/', got '{foo}'.")
    
    foo = FileTypes.home(None,'bat')
    if foo != '/bat':
        raise Exception(f"Regression 00110: FileTypes.home() should be '/bat'', got '{foo}'.")
    
    foo = FileTypes.home('zoom','bat')
    if foo != 'zoom/bat':
        raise Exception(f"Regression 00120: FileTypes.home() should be 'zoom/bat', got '{foo}'.")
    
    foo = FileTypes.home('/////zoom','bat/////')
    if foo != 'zoom/bat':
        raise Exception(f"Regression 00130: FileTypes.home() should be 'zoom/bat', got '{foo}'.")
    
    foo = FileTypes.home('zoom/////','/////bat')
    if foo != 'zoom/bat':
        raise Exception(f"Regression 00140: FileTypes.home() should be 'zoom/bat', got '{foo}'.")

    print("Testing Success.")  


if __name__ == '__main__':
    test_cases()  