# -*- coding: utf-8 -*-
import time
import logging
from chibi_site import Chibi_site
from chibi_browser.snippet import build_driver
from chibi_site.soup import Chibi_soup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger( 'chibi_browser' )


class Chibi_browser( Chibi_site ):
    build_driver_func = build_driver

    @property
    def browser( self ):
        try:
            return self._browser
        except AttributeError:
            logger.info( "contrullendo selenium driver" )
            self._browser = self.build_driver()
            logger.info( "abriendo navegador" )
            self._browser.get( self.url )
            return self._browser

    def build_driver( self, *args, **kw ):
        """
        wrapper para ser sobreescrito y poderle pasar los parametros al build
        """
        if 'download_folder' in self.kw:
            kw[ 'download_folder' ] = str( self.kw.download_folder )
        return self.build_driver_func( *args, **kw )

    def get( self, *args, **kw ):
        raise NotImplementedError

    def post( self, *args, **kw ):
        raise NotImplementedError

    def put( self, *args, **kw ):
        raise NotImplementedError

    def delete( self, *args, **kw ):
        raise NotImplementedError

    def download( self, path, *args, chunk_size=8192, **kw ):
        raise NotImplementedError

    @property
    def soup( self ):
        return Chibi_soup( self.browser.page_source, 'html.parser' )

    def reset( self, wait=0 ):
        if self.close():
            if wait:
                logger.info( f"esperando {wait} segundos antes de reiniciar" )
                time.sleep( wait )
            return self.browser

    def close( self ):
        try:
            self._browser.close()
            del self._browser
        except AttributeError:
            logger.warning(
                "el navegador no estaba abierto, se ignora close" )
            return False
        return True

    def refresh( self ):
        self.browser.refresh()

    def select( self, selector ):
        """
        atajo para buscar elementos con css

        find_elements( By.CSS_SELECTOR, selector )

        Parameters
        ----------
        selector: str
            selector de css con el que se buscaran elementos

        Returns
        -------
        WebElement
        """
        return self.browser.find_elements( By.CSS_SELECTOR, selector )

    def select_one( self, selector ):
        """
        atajo para buscar un elemento con css

        find_element( By.CSS_SELECTOR, selector )

        Parameters
        ----------
        selector: str
            selector de css con el que se buscaran elementos

        Returns
        -------
        WebElement
        """
        return self.browser.find_element( By.CSS_SELECTOR, selector )

    def wait( self, timeout=5, msg=None ):
        if msg:
            logger.info( msg )
        wait_driver = WebDriverWait( self.browser, timeout=timeout )
        return wait_driver

    @property
    def download_folder( self ):
        if 'download_folder' in self.kw:
            return self.kw.download_folder
        raise NotImplementedError(
            "no implementado cuando es el folder por default" )
