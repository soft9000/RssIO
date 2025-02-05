#!/usr/bin/env python3
# SecIO.py: Mission: Support URL content-security 'ops. 
# Rev 0.02
# Status: Tested.

'''THIS PROJECT IS INTENDED FOR USE WITH PUBLIC SECURITY PROTOCOLS. BE SURE TO UNDERSTAND 
THE RISK OF PRIVATELY PROTECTING YOUR CONTENT FROM GOVERNMENTAL EYES. DON'T DO ANYTHING 
THAT WILL LAND YOU IN PRISON!'''

from UrlIO import UrlParser

def to_hex(input_string):
    """
    Encodes a given string into its hexadecimal representation.
    
    :param input_string: The string to be encoded.
    :return: Hexadecimal encoded string.
    """
    return input_string.encode('utf-8').hex()

def from_hex(hex_string):
    """
    Decodes a given hexadecimal string back to its original string.
    
    :param hex_string: The hexadecimal string to be decoded.
    :return: Decoded original string.
    """
    return bytes.fromhex(hex_string).decode('utf-8')

def to_cotal(input_string):
    """Encodes a string to its octal representation."""
    return ' '.join(format(ord(char), 'o') for char in input_string)

def from_octal(octal_string):
    """Decodes an octal string back to its original representation."""
    return ''.join(chr(int(octal, 8)) for octal in octal_string.split())


class Enigma:
    '''Secured URL dection / creation with detected-content encoders / decoders.'''   
    PROTOCOL_DATA = { # procols should remain case-sensitive, please
        'DEFAULT' : [1000,'?default',   True],
        'OCTAL'   : [2000,'?octal',     True],
        'HEX'     : [3000,'?hex',       True],
        'LOCAL'   : [9000,'?local',     None]
        }
    
    PROTOCOL_KEYS = PROTOCOL_DATA.keys()    # Will superset - soon.
        
    def __init__(self, sec_key:str='DEFAULT'):
        if sec_key not in Enigma.PROTOCOL_KEYS:
            sec_key = 'DEFAULT'
        self.security = sec_key
        
    def detect(self, url)->str:
        '''Detect any security parameter. Security name Sec[key] whenever found + assigned.'''
        info = UrlParser.parse(url)
        if not UrlParser.is_null(info):
            for key in Enigma.PROTOCOL_DATA:
                if info['param'] == Enigma.PROTOCOL_DATA[key][1]:
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
        return url + Enigma.PROTOCOL_DATA[self.security][1]
    
    def identify(self)->int:
        '''Return the protocol number. -1 if not found.'''
        if not self.security:
            return -1
        which = Enigma.PROTOCOL_DATA[self.security]
        if not which:
            return -1
        return which[0]
    
    def encrypt(self, data:str)->str:
        '''Create a self-identifying encryption.'''
        token = f'.#[{self.security}]$.'
        return token + self.en(data) + token
    
    def decrypt(self, data:str)->str:
        '''Decrypt a self-identified encryption.'''
        token = f'.#[{self.security}]$.'
        cols = data.split(token)
        match len(cols):
            case 2|3:
                return self.de(cols[1])
        return data

    def en(self, data:str)->str:
        '''Encode the string, if possible. Returns unmodified string if protocol is not available.'''
        match self.identify():
            case 1000:
                pass
            case 2000:
                return to_cotal(data)
            case 3000:
                return to_hex(data)
            case 9000:
                pass               
        return data
    
    def de(self, data:str)->str:
        '''Encode the string, if possible. Returns unmodified string if protocol is not available.'''
        match self.identify():
            case 1000:
                pass
            case 2000:
                return from_octal(data)
            case 3000:
                return from_hex(data)
            case 9000:
                pass               
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
    spaces = '\n\r\t '   
    for ss, sec in enumerate(Enigma.PROTOCOL_KEYS):
        test = Enigma(sec)
        response = test.assign(web_site)
        if not response == responses[ss]:
            raise RssException(f"Regression #{ss}")
        if not sec == test.detect(response):
            raise RssException(f"Regression in detection for #{ss}")
        content = spaces + sec + spaces + sec + spaces
        if not test.de(test.en(content)) == content:
            raise RssException(f"Unable to cypher {sec}.")
    
        for dsample in responses:
            zcry = test.encrypt(dsample)
            zcry2 = test.decrypt(zcry)
            if not dsample == zcry2: 
                raise RssException(f"Unable to round-trip {sec}.")       
    
    print('Testing Success.')


if __name__ == '__main__':
    test_cases()
    