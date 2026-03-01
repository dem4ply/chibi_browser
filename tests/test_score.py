#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import unittest
from unittest.mock import patch
from chibi_browser import Chibi_browser
from chibi_browser import wait_conditions


class Test_chibi_browser_score_detector( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://antcpt.com/score_detector/'
        cls.browser = Chibi_browser( cls.url )

    def setUp( self ):
        self.browser.wait().until( wait_conditions.document.ready )

    def test_should_work( self ):
        self.assertTrue( self.browser.browser )
        time.sleep( 10 )

    def test_elements_should_have_score( self ):
        big = self.browser.select_one( 'div.well big' )
        self.assertTrue( big.text )

    def test_elements_should_have_refresh_score_button( self ):
        button = self.browser.select_one( 'div.well button' )
        self.assertTrue( button.text, 'Refresh score now!' )

    def test_click_should_work( self ):
        button = self.browser.select_one( 'div.well button' )
        button.click()

    @patch(
        "selenium.webdriver.common.action_chains.ActionChains.perform" )
    def test_click_should_call_action_perform( self, perform ):
        button = self.browser.select_one( 'div.well button' )
        button.click()
        perform.assert_called()
