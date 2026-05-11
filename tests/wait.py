#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import unittest
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
        self.browser.wait().until.document.ready()
        self.browser.show_mouse()

    def wait_score( self ):
        self.browser.wait().until(
            wait_conditions.element.select( "div.well big" ).wait(
                lambda x: x.text.lower().startswith( "your score is" ) ) )

    def test_should_work( self ):
        self.assertTrue( self.browser.browser )
        time.sleep( 1 )
