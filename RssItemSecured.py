from RssItemMeta import RSSItemMeta
from Content import ContentFile
from SecIO import Enigma


class RSSItemSecured(RSSItemMeta):
    '''A place to forever expand the possibilites (ad-hoc security, et al.) for RSSItemMeta.'''
    
    def __init__(self, user_json=None):
        super(RSSItemSecured, self).__init__(user_json)

    
    def en(self)->bool:
        '''Protect the ['text'].'''
        protocol = self.user_json['security']
        proto = Enigma(protocol)
        self.user_json['text'] = proto.en(self.user_json['text'])
        return True
    
    def de(self)->bool:
        '''Restore the ['text'].'''
        protocol = self.user_json['security']
        proto = Enigma(protocol)
        self.user_json['text'] = proto.de(self.user_json['text'])
        return True
 