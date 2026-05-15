from selenium.webdriver.support.ui import WebDriverWait
from chibi_browser import wait_conditions


class Wait:
    """
    se encarga de hacer los atajos para las fuciones wait_condition
    """
    def __init__( self, driver, timeout=5 ):
        self.driver = driver
        self.timeout = timeout

    def __call__( self, timeout=None, *args, **kw ):
        if timeout is None:
            timeout = self.timeout
        wait_driver = WebDriverWait(
            self.driver.browser, timeout=timeout )
        return wait_driver

    @property
    def until( self ):
        return Wait_until( self )


class Wait_until:
    def __init__( self, wait ):
        self.wait = wait

    @property
    def document( self ):
        return Document( self.wait )

    @property
    def element( self ):
        return Element( self.wait )

    def __call__( self, method, message="" ):
        self.wait().until( method, message=message )

    def is_true( self, method, message="" ):
        """
        espera a que la funcion regrese true

        Parameters
        ----------
        method: callable
        """
        self.wait().until( lambda x: method(), message=message )


class Basic_wait:
    def __init__( self, wait ):
        self.wait = wait


class Document( Basic_wait ):
    def ready( self ):
        """
        espera a que el documento este cargado
        """
        return self.wait.until( wait_conditions.document.ready )


class Element( Basic_wait ):
    @property
    def visible( self ):
        return Visible( self.wait )

    @property
    def invisible( self ):
        return Invisible( self.wait )


class Visible( Basic_wait ):
    def select( self, selector ):
        return self.wait.until(
            wait_conditions.element.visible.select( selector ) )


class Invisible( Basic_wait ):
    def select( self, selector ):
        return self.wait.until(
            wait_conditions.element.invisible.select( selector ) )
