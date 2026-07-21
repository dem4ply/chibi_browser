# -*- coding: utf-8 -*-
import time
import logging
from chibi_site import Chibi_site
from chibi_browser.snippet import (
    build_driver, add_mouse_to_selenium, hide_mouse_to_selenium,
)
from chibi_site.soup import Chibi_soup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .press_key import Press_key
from .wait import Wait


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
            logger.info( f"abriendo url: {self.url}" )
            self._browser.get( self.url )
            return self._browser

    def build_driver( self, *args, **kw ):
        """
        wrapper para ser sobreescrito y poderle pasar los parametros al build
        """
        if 'download_folder' in self.kw:
            kw[ 'download_folder' ] = str( self.kw.download_folder )
        if 'detach' in self.kw:
            kw[ 'detach' ] = bool( self.kw.detach )
        return self.build_driver_func( *args, **kw )

    def get( self, *args, **kw ):
        if not args and not kw:
            logger.info( f"abriendo url: {self.url}" )
            self.browser.get( self )
        else:
            raise NotImplementedError(
                "no esta implementado el get con argumentos" )

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
            # self._browser.close()
            self._browser.quit()
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

    def select_one( self, selector, func=None ):
        """
        atajo para buscar un elemento con css

        find_element( By.CSS_SELECTOR, selector )

        Parameters
        ----------
        selector: str
            selector de css con el que se buscaran elementos
        func: function
            funcion que se usara para filtrar los resultados

        Returns
        -------
        WebElement
        """
        if func is None:
            return self.browser.find_element( By.CSS_SELECTOR, selector )
        elements = self.select( selector )
        return next( filter( func, elements ) )

    def wait( self, timeout=5, msg=None ):
        """
        crea la clase de espera

        Examples
        --------
        Examples
        --------
        >>>browser = Chibi_browser( "https://antcpt.com/score_detector/" )
        >>>browser.wait().until.document.ready()
        >>>browser.wait().until(
            wait_conditions.element.select( "div.well big").wait(
            lambda x: "score" in x.text.lower() ) )
        """
        if msg:
            logger.info( msg )
        return Wait( self, timeout=timeout )
        wait_driver = WebDriverWait( self.browser, timeout=timeout )
        return wait_driver

    @property
    def download_folder( self ):
        if 'download_folder' in self.kw:
            return self.kw.download_folder
        raise NotImplementedError(
            "no implementado cuando es el folder por default" )

    def show_mouse( self ):
        add_mouse_to_selenium( self.browser )

    def hide_mouse( self ):
        hide_mouse_to_selenium( self.browser )

    @property
    def press_key( self ):
        return Press_key( self.browser )

    @property
    def cookies( self ):
        """
        regresa las cookies del navegador
        """
        return self.browser.get_cookies()

    @property
    def user_agent( self ):
        """
        regresa el user agent del navegador
        """
        return self.browser.execute_script( "return navigator.userAgent;" )
