from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class element:
    class visible:
        @staticmethod
        def select( selector ):
            return EC.visibility_of_element_located(
                ( By.CSS_SELECTOR, selector ) )

    class invisible:
        @staticmethod
        def select( selector ):
            return EC.invisibility_of_element_located(
                ( By.CSS_SELECTOR, selector ) )

    class clickable:
        @staticmethod
        def select( selector ):
            return EC.element_to_be_clickable(
                ( By.CSS_SELECTOR, selector ) )

    class select:
        def __init__( self, selector ):
            self.selector = selector

        def wait( self, func ):
            """
            Evalua usando la funcion con cada elemento del selector

            Parameters
            ----------
            func: funcion
                funcion que se usara para evaluar los elementos

            Examples
            --------
            >>>browser = Chibi_browser( "https://antcpt.com/score_detector/" )
            >>>browser.wait().until(
                wait_conditions.element.select( "div.well big").wait(
                lambda x: "score" in x.text.lower() ) )
            """
            selector = self.selector

            def predicate( driver ):
                elements = driver.find_elements( By.CSS_SELECTOR, selector )
                if not elements:
                    return False
                return any( func( element ) for element in elements )

            return predicate


class document:
    @staticmethod
    def ready( driver ):
        return driver.execute_script(
            "return document.readyState") == "complete"


class driver:
    class url:
        @staticmethod
        def startswith( expected_url ):
            def predicate( driver ):
                return driver.current_url.startswith( expected_url )
            return predicate

        def equal( expected_url ):
            def predicate( driver ):
                return driver.current_url == expected_url
            return predicate
