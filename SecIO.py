'''Mission: Support URL content-security 'ops. '''

from UrlIO import UrlParser

class Enigma:
    '''Secured URL dection / creation with detected-content encoders / decoders.'''   
    Sec = { # procols should remain case-sensitive, please
        'DEFAULT' : [1000,'?default',   None],
        'OCTAL'   : [2000,'?octal',     None],
        'HEX'     : [3000,'?hex',       None],
        'LOCAL'   : [9000,'?local',     None]
        }
    
    protocols = Sec.keys()
        
    def __init__(self, sec_key:str='DEFAULT'):
        if sec_key not in Enigma.protocols:
            sec_key = 'DEFAULT'
        self.security = sec_key
        
    def detect(self, url)->str:
        '''Detect any security parameter. Security name Sec[key] whenever found + assigned.'''
        info = UrlParser.parse(url)
        if not UrlParser.is_null(info):
            for key in Enigma.Sec:
                if info['param'] == Enigma.Sec[key][1]:
                    self.security = key
                    return key
        return None
    
    def assign(self, url)->str:
        '''Attach / replace a security parameter to the URL. None if not assigned, else encoding.'''
        if not url:
            return False
        pos = url.find('?')
        if not pos == -1:
            url = url[:pos]
        return url + Enigma.Sec[self.security][1]
    
    def en(self, data:str)->str:
        return data
    
    def de(self, data:str)->str:
        return data


def test_cases(debug=False):
    from RssExceptions import RssException;
    print(f"***** Testing Module {__name__}.")
    web_site = 'https://www.soft9000.com'
    test = Enigma()
    url = test.assign(web_site)
    if not url == 'https://www.soft9000.com?default':
        raise RssException("Assign Regression 1.0")
    if not test.detect(url) == 'DEFAULT':
        raise RssException("Detection Regression 1.1")
    if test.detect(None):
        raise RssException("Detection Regression 1.2")
    if test.detect(''):
        raise RssException("Detection Regression 1.3")
    if test.detect(web_site):
        raise RssException("Detection Regression 1.4")
    responses = [
        "https://www.soft9000.com?default",
        "https://www.soft9000.com?octal",
        "https://www.soft9000.com?hex",
        "https://www.soft9000.com?local"
    ]   
    for ss, sec in enumerate(Enigma.protocols):
        test = Enigma(sec)
        response = test.assign(web_site)
        if not response == responses[ss]:
            raise RssException(f"Regression #{ss}")
        if not sec == test.detect(response):
            raise RssException(f"Regression in detection for #{ss}")
    
    print('Testing Success.')


if __name__ == '__main__':
    test_cases()
    