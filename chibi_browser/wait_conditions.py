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


class document:
    @staticmethod
    def ready( driver ):
        return driver.execute_script(
            "return document.readyState") == "complete"
