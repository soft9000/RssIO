#!/usr/bin/env python3
# SecIO.py: Common File 'Meta. Some day to be properties when externalized.
# Rev 0.01
# Status: Lightly tested.

class FileTypes:
    SEP = '/'
    FT_TEMPLATE  = '.txt'   # RssTemplateFile.FILE_TYPE
    FT_OUT = '.html'        # NexusFile.FILE_TYPE
    FT_IN = '.json'         # ContentFile.FILE_TYPE
    DEFAULT_FILE_TEMPLATE   = "default" + FT_TEMPLATE
    DEFAULT_FILE_README     = 'README.txt'
    DEFAULT_FILE_RSS        = 'nexus.rss'
    
    @staticmethod
    def pop(node:str, sep=SEP)->str:
        '''Remove the last delimited node.'''
        if node:
            cols = node.split(sep)
            if len(cols) > 1:
                return sep.join(cols[:-1])
        return node

    @staticmethod
    def detox(node:str, sep=SEP)->str:
        if not node:
            return ''
        while node and node.startswith(sep):
            node = node[1:]
        while node and node.endswith(sep):
            node = node[:-1]
        if sep == '/':
            node = node.replace('\\','/')
        return node
    
    @staticmethod
    def fsdetox(node)->str:
        '''File-system normalizations'''
        if not node:
            return ''
        node = node.replace('\\', '/')
        return FileTypes.detox(node)

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
    print(f"***** Testing Module {__name__}.")
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
    
    if FileTypes.pop('1/2/3') != '1/2':
        raise Exception("Regression 00150: pop failure.")
    
    if FileTypes.pop('/1/2/3') != '/1/2':
        raise Exception("Regression 00160: pop failure.")
    
    print("Testing Success.")  


if __name__ == '__main__':
    test_cases()  