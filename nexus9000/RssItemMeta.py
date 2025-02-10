import email.utils
from Content import ContentFile

class RSSItemMeta:
    def __init__(self, user_json:dict=None):
        if not user_json:
            user_json = ContentFile.JSON_FIELD_SET
        else:
            for key in ContentFile.JSON_FIELD_SET:
                # superset / upgrade / add any missing keys
                if key not in user_json:
                    user_json[key] = ContentFile.JSON_FIELD_SET[key]
        self.json = dict(user_json)
    
    def assign(self,title, description, link, pubDate=None):
        '''Assign values - None becomes an empty string.'''
        if title is None:
            title=''
        self.json['title'] = title
        if description is None:
            description=''
        self.json['description']=description
        if link is None:
            link=''
        self.json['link']=link
        if pubDate is None:
            pubDate = ''
        self.json['pubDate']=pubDate        

    def is_robust(self):
        ''' A simple test to see if the item is ready for prime time.'''
        return self.json['title'] and self.json['link'] and self.json['description']
   
    def try_pubDate(self, date_str)->bool:
        ''' Attempt to set the pubDate. Return True if successful.'''
        try:
            _ = email.utils.parsedate_to_datetime(date_str)
            self.json['pubDate'] = date_str
            return True
        except:
            return False

    @property
    def title(self):
        return self.json['title']

    @title.setter
    def title(self, value):
        if value is None: value=''
        self.json['title'] = value

    @property
    def link(self):
        return self.json['link']

    @link.setter
    def link(self, value):
        if value is None: value=''
        self.json['link'] = value

    @property
    def description(self):
        return self.json['description']

    @description.setter
    def description(self, value):
        if value is None: value=''
        self.json['description'] = value

    @property
    def pubDate(self):
        return self.json['pubDate']

    @pubDate.setter
    def pubDate(self, value):
        if value is None: value=''
        self.json['pubDate'] = value