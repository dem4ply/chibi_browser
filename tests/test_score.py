#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import unittest
from unittest.mock import patch
from chibi_browser import Chibi_browser
from chibi_browser import wait_conditions


def rand_xy():
    return random.random() * 500, random.random() * 500


class Test_chibi_browser_score_detector( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = "https://antcpt.com/score_detector/"
        cls.browser = Chibi_browser( cls.url )

    def setUp( self ):
        super().setUp()
        self.browser.wait().until( wait_conditions.document.ready )
        self.browser.show_mouse()

    def wait_score( self ):
        self.browser.wait().until(
            wait_conditions.element.select( "div.well big" ).wait(
                lambda x: x.text.lower().startswith( "your score is" ) ) )

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
        self.wait_score()
        button.click()
        time.sleep( 3 )

    def test_selector_with_lambda_should_return_expected( self ):
        self.wait_score()
        clear_button = self.browser.select_one(
            "div.well button",
            lambda x: 'clear' in x.text.lower() )
        self.assertEqual( clear_button.text.lower(), 'clear list' )

    def test_move_and_click_score( self ):
        self.wait_score()
        score_button = self.browser.select_one( 'div.well button' )
        header = self.browser.select_one( 'blockquote' )
        clear_button = self.browser.select_one(
            "div.well button",
            lambda x: 'clear' in x.text.lower() )

        for i in range( 5 ):
            score_button.hover_mouse( random_coficient=1 )
            header.hover_mouse( random_coficient=1 )
            clear_button.hover_mouse( random_coficient=1 )

    @patch(
        "selenium.webdriver.common.action_chains.ActionChains.perform" )
    def test_click_should_call_action_perform( self, perform ):
        button = self.browser.select_one( 'div.well button' )
        button.click()
        perform.assert_called()
