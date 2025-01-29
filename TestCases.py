#!/usr/bin/env python3
# Core test cases.

from RssIO          import test_cases as tc_RssIO
from RssNexus       import test_cases as tc_RssNexus
from NexusProject   import test_cases as tc_NexusProject

tc_RssIO()
tc_RssNexus()
tc_NexusProject()