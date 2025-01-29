# Overview
Two different workflows here:

First - and as expected - we simply need to create + manage a default RssProject.

Secondly - and a tad more complex - we need to update an existing RSS site. 
For reasons of simplicity we're assuming we've created it. 

File.FileTypes is presently hard-coded... also saved time.

# RssIO
A Pythonic way to read, write, and manage as many Really Simply Syndications as possible.

# RssNexus
A faster / less error prone way to  skin & RSS our content. Perfect for static websites.

The idea is simple: We'll add any type of file into an input folder, define as many skins in the template folder as we require, then use RSSNexus to burn the final content to the output folder.

Once burned to the output folder the RSS file therein will link to the same.

# NexusProject
RssSite is presently a work in progress. Everything else is o.k for you to use in your own.

RssSite is much like RssNexus, but RssSite adds an official set of hard-wired assumptions.

An RssSite is designed read any single `input` folder, skin the text using any input-defined 
`template` file, then place the results into a single `output` folder. 
    
Ready to upload to your site, the `output` folder will also contain the `nexus.rss` file.

A default template is provided. Feel free to change it and / or create your own template file(s) 
to use from within your `input` file updates.

# Test Cases
... tell what's whut, thus far.
