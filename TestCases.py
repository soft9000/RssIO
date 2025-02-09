#!/usr/bin/env python3
# Core test cases.

from Files          import test_cases as tc_Files
from SecIO          import test_cases as tc_SecIO
from UrlIO          import test_cases as tc_UrlIO
from RssIO          import test_cases as tc_RssIO
from Content        import test_cases as tc_Content
from RssNexus       import test_cases as tc_RssNexus
from NexusScout     import test_cases as tc_NexusScout
from Nexus          import test_cases as tc_NexusProject
from bloogle        import test_cases as tc_TUI

tc_UrlIO()
tc_SecIO()
tc_Files()
tc_Content()
tc_RssIO()
tc_RssNexus()
tc_NexusProject()
tc_NexusScout()
tc_TUI()