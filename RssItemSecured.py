from RssItemMeta import RSSItemMeta
from Content import ContentFile


class RSSItemSecured(RSSItemMeta):
    '''A place to forever expand the possibilites (ad-hoc security, et al.) for RSSItemMeta.'''
    
    def __init__(self, user_json=None):
        if not user_json:
            user_json = ContentFile.DEFAULTS
        else:
            for key in ContentFile.DEFAULTS:
                # superset / upgrade / add any missing keys
                if key not in user_json:
                    user_json[key] = ContentFile.DEFAULTS[key]
        super(user_json['title'], user_json['description'], user_json['link'], user_json['pubDate'])
        self.user_json = user_json
    
    def en(self)->bool:
        '''Protect the ['text'].'''
        protocol = self.user_json['security']
        proto = RSSItemSecured(protocol)
        self.user_json['text'] = proto.en(self.user_json['text'])
        return True
    
    def de(self)->bool:
        '''Restore the ['text'].'''
        protocol = self.user_json['security']
        proto = RSSItemSecured(protocol)
        self.user_json['text'] = proto.de(self.user_json['text'])
        return True
 