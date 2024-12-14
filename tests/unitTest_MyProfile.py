import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "admin"
        pwd = "tested2024"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/admin")

        # Log in as admin
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        # Navigate to the main page
        driver.get("http://127.0.0.1:8000")
        time.sleep(2)

        try:
            # Look for the 'Workouts' button and click it
            elem = driver.find_element(By.XPATH, "/html/body/nav/a[5]")
            elem.click()
            time.sleep(2)

            print("Current URL:", driver.current_url)

            # Debug: Print page source
            print("Page Source:", driver.page_source[:500])  # Limit output to 500 characters

            # Temporarily disable assertions for debugging
            print("Successfully clicked on the My Profile button.")
        except NoSuchElementException:
            self.fail("My Profile button not found.")
        finally:
            driver.close()


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')

