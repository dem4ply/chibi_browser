#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
from chibi_browser import Chibi_browser
from chibi_browser.snippet import wait_to_browser_close, build_chrome
from selenium.common.exceptions import SessionNotCreatedException


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


class Test_build_chrome_with_detach( unittest.TestCase ):

    def setUp( self ):
        patcher_chrome = patch( 'chibi_browser.snippet.webdriver.Chrome' )
        self.mock_chrome = patcher_chrome.start()
        self.addCleanup( patcher_chrome.stop )

        patcher_options = patch( 'selenium.webdriver.chrome.options.Options' )
        self.mock_options_cls = patcher_options.start()
        self.addCleanup( patcher_options.stop )
        self.mock_options = Mock()
        self.mock_options_cls.return_value = self.mock_options

    def test_without_detach_should_not_call_add_experimental( self ):
        build_chrome( detach=False )

        self.mock_options.add_experimental_option.assert_not_called()
        self.mock_chrome.assert_called_once_with(
            options=self.mock_options )

    def test_with_detach_should_add_debugger_address( self ):
        build_chrome( detach=True )

        self.mock_options.add_experimental_option.assert_any_call(
            "debuggerAddress", "127.0.0.1:9222" )
        self.mock_chrome.assert_called_once_with(
            options=self.mock_options )

    def test_with_detach_and_session_exception_should_create_start_new( self ):
        self.mock_chrome.side_effect = [
            SessionNotCreatedException( "no se pudo conectar" ),
            Mock(),
        ]

        build_chrome( detach=True )

        self.assertEqual( self.mock_chrome.call_count, 2 )

        # primer intento: attach por debuggerAddress
        first_option = self.mock_options.add_experimental_option
        first_option.assert_any_call(
            "debuggerAddress", "127.0.0.1:9222" )

        # segundo intento: nueva sesion con remote-debugging-port
        second_option = self.mock_options_cls.return_value
        second_option.add_argument.assert_any_call(
            "--remote-debugging-port=9222" )

    def test_with_detach_driver_should_have_chibi_web_element( self ):
        from chibi_browser.web_element import Chibi_web_element
        driver = build_chrome( detach=False )
        self.assertEqual( driver._web_element_cls, Chibi_web_element )
