#!/usr/bin/env python3
# Core test cases.

from Files          import test_cases as tc_Files
from RssIO          import test_cases as tc_RssIO
from Content        import test_cases as tc_Content
from RssNexus       import test_cases as tc_RssNexus
from NexusProject   import test_cases as tc_NexusProject

tc_Files()
tc_Content()
tc_RssIO()
tc_RssNexus()
tc_NexusProject()