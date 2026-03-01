#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import unittest
from chibi.file.temp import Chibi_temp_path
from chibi_browser import Chibi_browser
from chibi_browser import wait_conditions


class Test_download( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.url = 'https://archive.org/details/harvest-moon-ranch-master'
        cls.browser = Chibi_browser(
            cls.url, download_folder=Chibi_temp_path() )

    @classmethod
    def tearDownClass( cls ):
        cls.browser.close()

    @unittest.skip( "debug when is not changing download folder" )
    def test_check_settings( self ):
        self.browser.browser.get( 'chrome://settings/?search=download' )
        import pdb
        pdb.set_trace()
        pass

    def test_download_torrent( self ):
        # self.browser.select_one( "div.show-all a.boxy-ttl" ).click()
        links = self.browser.select( "div.show-all a.boxy-ttl" )
        for link in links:
            if link.text.lower().strip() == 'show all':
                link.click()
                break
        self.browser.wait( 10 ).until(
            wait_conditions.element.visible.select(
                "table.directory-listing-table" ) )
        table = self.browser.select_one( "table.directory-listing-table" )
        files = table.select( 'a' )
        for f in files:
            if '.torrent' in f.text:
                f.click()

        time.sleep( 2 )
        files = list( self.browser.download_folder.ls() )
        self.assertTrue( files )
