#!/usr/bin/env python3
# rss9000.py: A TUI destined to manage a nexus of RSS sites, templates, and more.
# Rev 0.01
# Status: R&D.
import logging
import argparse

from Content import ContentFile
import NexusScout
from Nexus import RSSSite
from RssItemSecured import RSSItemSecured

logfile = ContentFile.ALL_PROJECTS + "rssio.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def lprint(msg:str, level=logging.INFO):
    '''Log + print a message.'''
    print(msg)
    logging.log(level, msg)


def create(args):
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


def list(args):
    aite = NexusScout.locate_sites(args.site)
    if not aite:
        print(f"No sites defined in `{ContentFile.ALL_PROJECTS}` ...")
        return True # yes - op is ok.
    print(f"Sites under `{ContentFile.ALL_PROJECTS}` ...")
    for i, line in enumerate(aite,1):
        print(f"[{i:^4}] {line.url}")
    return True


def topic(args):
    if not args.site:
        print("Error: Site URL is required for RssIO topic generation.")
        return False
    site = RSSSite(args.site)
    if not site.folders_exist():
        print(f"Error: Input '{args.site}' has not been created.")
        return False
    filename = site.cf_create_default()
    if not filename:
        lprint(f"Error: Unable to create topic template for {args.site}.")
        return False
    lprint(f"Success: Default input topic generated for {args.site}.")
    return True


def merge(args):
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
    
    
def main():
    '''Basic TUI R&D.'''
    parser = argparse.ArgumentParser(description='Manage Really Simple Syndication (R.S.S) Feeds.')
    parser.add_argument('operation', choices=['create', 'list', 'merge', 'topic'], help='RSS operations')
    parser.add_argument('--site', default=None, help='Site name / URL')

    args = parser.parse_args()

    if args.operation == 'create':
        return create(args)

    elif args.operation == 'list':
        return list(args)

    elif args.operation == 'topic':
        return topic(args)

    elif args.operation == 'merge':
        return merge(args)
  
    parser.print_help()
    
def test_cases(debug=False):
    args = argparse.ArgumentParser()
    args.site = "http://Zite9000.org"
    create(args)
    list(args)
    topic(args)
    if not debug:
        site = RSSSite(args.site)
        if not site.rmtree():
            print(f"Error: Unable to remove '{args.site}'")
        else:
            print("Test project successfully deleted.")


if __name__ == '__main__':
    debug = True
    if not debug:
        if main():
            print("\t- Happy Bloogling!")
    else:
        test_cases(False)

