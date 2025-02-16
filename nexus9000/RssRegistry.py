import os.path
from Files import FileTypes
import NexusScout

class FreeRegistry:
    '''
    Registration is optional. Merging your local `registry.txt` to the RssIO 
    Project on GitHub allows others to discover your site.
    '''

    def __init__(self, registry='registry.txt'):
        self.registry = registry
    
    def total(self):
        file = self.get_registry_file()
        try:
            with open(file) as fh:
                return len(fh.readlines())
        except:
            pass
        return 0        
        
    def delete_registry(self)->bool:
        file = self.get_registry_file()
        try:
            os.unlink(file)
            return not os.path.exists(file)
        except:
            return False
    
    def get_registry_file(self)->str:
        root = FileTypes.pop(FileTypes.detox(__file__))
        if not os.path.exists(root):
            return None
        return FileTypes.home(root, self.registry)

    def register(self):
        '''
        Registration is optional. Merging your local `registry.txt` to the RssIO 
        Project allows others to discover your site.
        '''
        if not __file__:
            return False, 'Unable to locate module __file__.'
        aite = NexusScout.locate_sites()
        if not aite:
            return False, 'No sites found.'
        registry = self.get_registry_file()
        if not registry:
            return False, f'Unable to create {self.registry}'
        mode = 'w'
        sites = [a.url for a in aite]
        try:
            if os.path.exists(registry):
                mode = 'a'
                with open(registry, 'r') as fh:
                    for line in fh:
                        base = line.strip() 
                        if base in sites:
                            sites.remove(base)
                            if not sites: return True, "All sites registered"
                            continue
            with open(registry, mode) as fh:
                print(*sites,sep='\n',file=fh)
            return True, f"Registered {len(aite)} additional sites in {registry}."
        except Exception as ex:
            return False, str(ex)

def test_cases(debug=False):
    print(f"***** Testing Module {__name__}.")
    import Nexus
    from RssExceptions import RssException
    sites = [
    Nexus.RSSSite('http://www.soft9000.com'),
    Nexus.RSSSite('http://www.soft9001.com'),    
    Nexus.RSSSite('http://www.soft9002.com'),
    ]
    sites2 = [
    Nexus.RSSSite('http://www.soft9003.com'),
    Nexus.RSSSite('http://www.soft9004.com'),    
    Nexus.RSSSite('http://www.soft9005.com'),
    ]
    all_sites = [*sites, *sites2]
    for site in all_sites:
        site.rmtree() # Clean-up any previous test cases

    test = FreeRegistry('~test_registry.txt')
    test.delete_registry()
    
    for site in sites:
        if not site.setup():
            raise RssException(f"Unable to create test site {site}.")
        '''if not site.cf_create_default():
            raise RssException(f"Unable to create test content for site {site}.")
        if not site.update():
            raise RssException(f"Unable to merge test content for {site}.")'''
    info = test.register()
    if not info[0]:
        raise RssException(f"Test case failure {info[1]}")
    
    if test.total() != 3:
        raise RssException("Registration failure #1.")
    for site in sites:
        site.setup()
        
    info = test.register()
    if test.total() != 3:
        raise RssException("Registration failure #2.")

    for site in sites2:
        if not site.setup():
            raise RssException(f"Unable to create test site {site}.")
        
    info = test.register()
    if test.total() != 6:
        raise RssException("Registration failure #3.")        
    if not debug:
        for site in all_sites:
            if not site.rmtree():
                raise RssException("Unable to remove test sites.")
        if not test.delete_registry():
            raise RssException(f"Unable to remove {test.get_registry_file()}")

    print("Testing Success.")


if __name__ == '__main__':
    test_cases()



