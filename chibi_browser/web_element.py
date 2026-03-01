import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


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

    def click( self, *, random_coficient=0 ):
        """
        mueve el mouse a la pocicion del elemento y hace click usando actions

        usando los actionschain
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
