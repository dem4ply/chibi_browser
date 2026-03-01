#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi_browser import Chibi_browser
from chibi_browser.snippet import wait_to_browser_close


class Test_wait_until_close_timeout( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://www.google.com'
        cls.browser = Chibi_browser( cls.url )

    def test_wait_until_close_should_work_with_timeout( self ):
        wait_to_browser_close( self.browser, timeout=1 )


@unittest.skip( "need human input" )
class Test_wait_until_close( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://www.google.com'
        cls.browser = Chibi_browser( cls.url )

    def test_wait_until_close_should_wait( self ):
        print( "cierra el navegador de manera manual" )
        wait_to_browser_close( self.browser )
