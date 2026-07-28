#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi_browser import Chibi_browser
from chibi_browser.web_element import Chibi_web_element


class Test_web_element( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://archive.org/details/harvest-moon-ranch-master'
        cls.browser = Chibi_browser( cls.url )

    def test_driver_should_be_chibi_web_element( self ):
        self.assertEqual(
            self.browser.browser._web_element_cls, Chibi_web_element )

    def test_select_with_attributes_should_be_a_list( self ):
        self.browser.get()
        result = self.browser.select(
            'a[rel~="ugc"]', with_attributes={ 'rel': 'ugc' } )
        self.assertIsInstance( result, list )

    def test_driver_should_have_the_same_elements( self ):
        self.browser.get()
        result = self.browser.select(
            'a', with_attributes={ 'rel': 'ugc' } )
        result_2 = self.browser.select( 'a[rel~="ugc"]', )
        self.assertEqual( len( result ), len( result_2 ) )
