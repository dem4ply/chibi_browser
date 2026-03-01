#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi_browser import Chibi_browser
from selenium.webdriver.chrome.webdriver import WebDriver as chrome_driver


class Test_chibi_browser( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://www.google.com'
        cls.browser = Chibi_browser( cls.url )

    @classmethod
    def tearDownClass( cls ):
        cls.browser.close()

    def test_should_work( self ):
        self.assertTrue( self.browser )

    def test_broser_instance_should_be_selenium_driver( self ):
        driver = self.browser.browser
        self.assertIsInstance( driver, chrome_driver )

    def test_url_should_be_the_expected( self ):
        driver = self.browser.browser
        self.assertTrue( driver.current_url.startswith( self.url ) )

    def test_browser_property_should_return_the_same_instance( self ):
        driver1 = self.browser.browser
        driver2 = self.browser.browser
        self.assertIs( driver1, driver2 )

    def test_soup_should_no_be_empty( self ):
        soup = self.browser.soup
        self.assertTrue( str( soup ) )

    def test_reset_browser_should_create_new_instance( self ):
        driver1 = self.browser.browser
        self.browser.reset()
        driver2 = self.browser.browser
        self.assertIsNot( driver1, driver2 )

    def test_refresh_should_not_create_new_browser( self ):
        driver1 = self.browser.browser
        self.browser.refresh
        driver2 = self.browser.browser
        self.assertIs( driver1, driver2 )
