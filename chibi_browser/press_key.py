from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Press_key:
    def __init__( self, driver ):
        self._driver = driver

    def _send_key( self, key ):
        ActionChains( self._driver ).send_keys( key ).perform()

    def esc( self ):
        self._send_key( Keys.ESCAPE )

    def end( self ):
        self._send_key( Keys.END )

    def page_down( self ):
        self._send_key( Keys.PAGE_DOWN )
