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

    def __call__( self, method, message="" ):
        self.wait().until( method, message=message )


class Document:
    def __init__( self, wait ):
        self.wait = wait

    def ready( self ):
        """
        espera a que el documento este cargado
        """
        return self.wait.until( wait_conditions.document.ready )
