import logging
import datetime
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from chibi_browser.web_element import Chibi_web_element


logger = logging.getLogger( 'chibi_browser.snipepts' )


def build_chrome( *args, download_folder=None ):
    options = Options()
    if download_folder:
        options.add_experimental_option(
            'prefs', {
                # Change default directory for downloads
                "download.default_directory": download_folder,
                "savefile.default_directory": download_folder,
                # To auto download the file
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                # It will not show PDF directly in chrome
                "plugins.always_open_pdf_externally": True
            }
        )
    # options.add_argument( "--headless=new" )
    driver = webdriver.Chrome( options=options )
    driver._web_element_cls = Chibi_web_element
    return driver


def build_undetected_chrome( *args, download_folder=None ):
    import undetected as uc

    options = Options()
    if download_folder:
        options.add_experimental_option(
            'prefs', {
                "download.default_directory": download_folder,
                "savefile.default_directory": download_folder,
                "download.prompt_for_download": False,
            } )
    # options.add_argument( "--headless=new" )
    desire_capabilities = DesiredCapabilities.CHROME
    desire_capabilities[ 'pageLoadStrategy' ] = 'eager'
    driver = uc.Chrome( version_main=145, options=options )
    """
    driver = uc.Chrome(
        version_main=145,
        desired_capabilities=desire_capabilities, options=options )
    """
    driver._web_element_cls = Chibi_web_element
    return driver


def build_driver( *args, **kw ):
    return build_chrome( *args, **kw )
    return build_undetected_chrome( *args, **kw )


def wait_to_browser_close( browser, timeout=None ):
    start = datetime.datetime.utcnow()
    from chibi_browser import Chibi_browser
    if isinstance( browser, Chibi_browser ):
        browser = browser.browser
    while True:
        try:
            _ = browser.window_handles
        except selenium.common.exceptions.InvalidSessionIdException:
            logger.info( "se detecto que el navegador fue cerrado" )
            break
        time.sleep( 1 )
        if timeout:
            current = datetime.datetime.utcnow()
            delta = current - start
            if delta.total_seconds() > timeout:
                break
