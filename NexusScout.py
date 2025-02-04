        
#!/usr/bin/env python3
# NexusScout.py: An RSSSite location service.
# Rev 0.00
# Status: R&D.
import os

from Content import ContentFile
from Nexus import RSSSite

def locate_sites(root=ContentFile.ALL_PROJECTS, nexi=RSSSite.RSS_NODE)->list:
    '''Look for RSS files. Returns a list of RSSSite if any located in `root.` Empty list if none located..'''
    results = []
    if not root or not nexi:
        return results
    for root, _, files in os.walk(root):
        for file in files:
            if file == nexi:
                results.append(RSSSite(root + '/' + file))
    return results

def test_cases(debug=False):
    from RssExceptions import RssException
    sites = []
    
    print(f"***** Testing Module {__name__}.")
    # STEP: Default Site Creation + Load + Existance

    for dum in 'testa', 'TestB', 'tEStC':
        tsite = f'http://www.{dum}.org'
        rss_str = f"""<?xml version="1.0" ?>
    <rss version="2.0">   
    <channel>
        <title>Channel / Site Title</title>
        <link>https://www.{dum}.org/nexus.rss</link>
        <description>Description of this RSS channel or site</description>
        <generator>https://github.com/soft9000/RssIO</generator>
    </channel>
    </rss>"""        
        site = RSSSite(tsite,f"https://www.{dum}.foo")
        if not site.setup():
            raise RssException('Site creation failure.')
        if not site.rss_replace(rss_str):
            pass
        feed = site.read_feed()
        if not feed:
            raise RssException(f'Unable to RssSite.read_feed({tsite}).')
        
        if not site.folders_exist():
            raise RssException("RssSite.exists() failure.")
        
        sites.append(site)

    # STEP: Remove Test Site / Reset Test Case
    for site in sites:
        if not debug and not site.rmtree():
            raise RssException("Regression: Unable to remove test site.")
    print("\nTesting Success.")


if __name__ == '__main__':
    test_cases()
    