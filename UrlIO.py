from urllib.parse import urlparse
'''A little effort designed to enforce a reasonable set of logic to enable plug-in URL security options. '''

class UrlParser:
    DEFAULT_FIELDS = {
        "scheme": None,
        "site": None,
        "path": None,
        "param": None,
        "query": None,
        "fragment": None
    }
    
    @staticmethod
    def default(param:str)->str:
        if not param:
            return None
        return param
    
    @staticmethod
    def is_null(parsed:dict)->bool:
        try:
            count = 0
            for key in parsed:
                if parsed[key] is not None:
                    count = count + 1
            return count == 0
        except:
            pass
        return True

    @staticmethod
    def parse(url)->dict:
        '''Always returns a DEFAULT_FIELDS. Any `None`` field therin indicates failure.'''
        result = dict(UrlParser.DEFAULT_FIELDS)
        if not url:
            return result
        parsed_url = urlparse(url)
        result['scheme'] = UrlParser.default(parsed_url.scheme)
        result['site'] = UrlParser.default(parsed_url.netloc)
        result['path'] = UrlParser.default(parsed_url.path)
        result['param'] = UrlParser.default(parsed_url.params)
        result['query'] = UrlParser.default(parsed_url.query)
        result['fragment'] = UrlParser.default(parsed_url.fragment)
        if not result['param']:
            pos = url.find('?')
            if pos != -1:
                result['param'] = url[pos:].strip()
        return result


def test_cases(debug=False):
    print(f"***** Testing Module {__name__}.")
    UrlParser.is_null(None)
    responses = [
        {'scheme': None, 'site': None, 'path': None, 'param': None, 'query': None, 'fragment': None},
        {'scheme': None, 'site': None, 'path': None, 'param': None, 'query': None, 'fragment': None},
        {'scheme': 'https', 'site': 'www.soft9000.com', 'path': None, 'param': None, 'query': None, 'fragment': None},
        {'scheme': 'https', 'site': 'www.example.com', 'path': '/path/to/page', 'param': '?name=JohnDoe&age=25#section1', 'query': 'name=JohnDoe&age=25', 'fragment': 'section1'},
    ]
    for ss, result in enumerate([None, '', 
                                 'https://www.soft9000.com',
                                 'https://www.example.com/path/to/page?name=JohnDoe&age=25#section1']):
        response = UrlParser.parse(result)
        if ss > 1:
            if UrlParser.is_null(response):
                raise Exception(f"Regression: #{ss} should not be null.")
        for key in responses[ss]:
            if not response[key] == responses[ss][key]:
                print(response)
                raise Exception(f'Regresson #{ss}.')

    print("Testing Success.")


if __name__ == '__main__':
    test_cases()

