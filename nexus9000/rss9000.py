#!/usr/bin/env python3
# rss9000.py: A TUI destined to manage a nexus of RSS sites, templates, and more.
# Rev 0.01
# Status: R&D.
import logging
import argparse

from Content import ContentFile
import NexusScout
from Nexus import RSSSite
from RssRegistry import FreeRegistry
from RssItemSecured import RSSItemSecured

logfile = ContentFile.ALL_PROJECTS + "rssio.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def input_verify(prompt:str)->str:
    response = input(prompt)
    yn = input(f'{response} [y/N]: ')
    if not yn:
        return yn
    if yn.lower() == 'y':
        return response
    return None


def intput_verify(prompt:str='> ', defval=-1)->str:
    response = input(prompt)
    try:
        return int(response)
    except:
        return defval


def lprint(msg:str, level=logging.INFO):
    '''Log + print a message.'''
    print(msg)
    logging.log(level, msg)


def create(args)->bool:
    '''Create a web site in {ContentFile.ALL_PROJECTS}.'''
    if not args.site:
        print("Error: Site URL is required for RssIO site creation.")
        return False
    if not RSSSite.is_url(args.site):
        print(f"Error: '{args.site}' is not a supported RssIO site name.")
        return False
    site = RSSSite(args.site)
    if not site.setup():
        print(f"Error: Unable to create '{args.site}'. Please insure file system access.")
        return False
    if not site.update():
        print(f"Error: Unable to generate '{args.site}'. Please insure file system access.")
        return False
    lprint(f"Created '{args.site}'")
    print(f'You can now manage files in the input folder for {site.home_dir}.')
    print(f'See the README.txt file within that folder for more information.')
    return True


def slist(args)->bool:
    '''Locate and list web sites under {ContentFile.ALL_PROJECTS}.'''
    aite = NexusScout.locate_sites()
    if not aite:
        print(f"No sites defined in `{ContentFile.ALL_PROJECTS}` ...")
        return True # yes - op is ok.
    print(f"Sites under `{ContentFile.ALL_PROJECTS}` ...")
    for i, line in enumerate(aite,1):
        print(f"[{i:^4}] {line.url}")
    return True


def topic(args,topic:str=None)->bool:
    '''Create an input topic file.'''
    if not args.site:
        print("Error: Site URL is required for RssIO topic generation.")
        return False
    site = RSSSite(args.site)
    if not site.folders_exist():
        print(f"Error: Input '{args.site}' has not been created.")
        return False
    if not topic:
        topic = input_verify("Site subfolder: ")
    filename = site.cf_create_default(topic)
    if not filename:
        lprint(f"Error: Unable to create topic template for {args.site}.")
        return False
    lprint(f"Success: Default input topic generated for {args.site}.")
    return True


def merge(args)->bool:
    '''Convert site input to site output.'''
    if not args.site:
        print("Error: Site URL is required for RssIO content generation.")
        return False
    if not RSSSite.is_url(args.site):
        print(f"Error: '{args.site}' is not a supported RssIO site name.")
        return False
    site = RSSSite(args.site)
    if not site.update():
        lprint(f"Error: Unable to merge content for {args.site}.")
        return False
    lprint(f"Success: Merged content generated for {args.site}.")
    return True


def register(args)->bool: # TODO: TUI test this!
    '''Add your site(s) to the RssIO Registry File.'''
    if False:
        info = FreeRegistry().register()
        if info[0]:
            lprint(info[1])
            return True
        else:
            print(info[1])
            return False
    else:
        print("Toto - Work in progress.")
        return False


def mainloop():
    print("Site Management Loop")
    ops = {
        "Create":[create,True],
        "List":[slist, False],
        "Topic":[topic, True],
        "Merge":[merge,True],
        "Register":[register,True],
        "Quit":[quit, False] # always last, please
    }
    while True:
        for ss, op in enumerate(ops,1):
            print(f'{ss}.) {op}: {ops[op][0].__doc__}')
        which = intput_verify()
        if which == -1:
            which = input("Quit? Y/n")
            if not which or which.lower()[0] == 'y':
                print("Done - Happy Rssing!")
                return True
            print("...")
            continue
        if which > 0 and which <= len(ops.keys()):
            if which == len(ops):   # last 'op
                ops['Quit'][0]()
            args = argparse.ArgumentParser()
            args.site = None
            keys = list(ops.keys())
            key = keys[which-1]
            func = ops[key]

            if func[1]:
                site = input_verify("Site: ")
                if not site:
                    continue
                args.site = site                
            func[0](args)
            continue
        print(f"#{which} is not a valid option.")
    
    
def main():
    '''Basic TUI'''
    parser = argparse.ArgumentParser(description='Manage Really Simple Syndication (R.S.S) Feeds.')
    parser.add_argument('--op', choices=['create', 'list', 'merge', 'topic', 'register'], help="Site Management 'Ops")
    parser.add_argument('--site', default=None, help='Site name / URL')

    args = parser.parse_args()

    if args.op == 'create':
        return create(args)

    elif args.op == 'list':
        return slist(args)

    elif args.op == 'topic':
        return topic(args)

    elif args.op == 'merge':
        return merge(args)

    elif args.op == 'register':
        return merge(args)
      
    parser.print_help()
    
    # Just loop it:
    print('~' * 12)
    br = mainloop()
    print('~' * 12)
    return br

    
def test_cases(debug=False):
    args = argparse.ArgumentParser()
    args.site = "http://Zite9000.org"
    create(args)
    slist(args)
    topic(args,'test_topic_dir')
    if not debug:
        site = RSSSite(args.site)
        if not site.rmtree():
            print(f"Error: Unable to remove '{args.site}'")
        else:
            print("Test project successfully deleted.")

    


if __name__ == '__main__':
    debug = False
    if not debug:
        if main():
            print("\t- Happy Rssing!")
    else:
        test_cases(False)

