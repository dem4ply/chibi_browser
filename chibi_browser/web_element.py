import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from chibi_atlas import Chibi_atlas
from humancursor import WebCursor


class Chibi_web_element( WebElement ):
    @property
    def driver( self ):
        """
        regresa el web driver del cual se obtubo el elemento
        """
        return self._parent

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
        return self.find_elements( By.CSS_SELECTOR, selector )

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
        return self.find_element( By.CSS_SELECTOR, selector )

    def hover_mouse( self, *, random_coficient=0 ):
        self.sleep( random_coficient )
        self.human.move_to( self )
        actions = ActionChains( self.driver )
        actions.move_to_element( self ).perform()

    def scroll_to_view( self, *, random_coficient=0 ):
        self.sleep( random_coficient )
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", self
        )

    def click( self, *, simple=False, random_coficient=0 ):
        """
        mueve el mouse a la pocicion del elemento y hace click
        """
        if simple:
            super().click()
            return
        self.hover_mouse( random_coficient=random_coficient )
        self.sleep( random_coficient )
        self.human.click()

        """
        if random_coficient:
            random_time = random_coficient * random.random()
            time.sleep( random_time )

        actions = ActionChains( self.driver )
        actions.move_to_element( self ).perform()
        if random_coficient:
            random_time = random_coficient * random.random()
            time.sleep( random_time )
        actions.click( self ).perform()
        """

    def sleep( self, random_coficient ):
        random_time = random_coficient * random.random()
        time.sleep( random_time )

    @property
    def attrs( self ):
        from chibi_browser.snippet import js_get_all_attrs
        attributes = self.run_script( js_get_all_attrs )
        return Chibi_atlas( attributes )

    def run_script( self, js_script ):
        return self.driver.execute_script( js_script, self )

    @property
    def human( self ):
        try:
            return self._human
        except AttributeError:
            self._human = WebCursor( self.driver )
            return self._human
