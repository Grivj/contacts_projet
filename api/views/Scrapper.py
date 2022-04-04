from flask_restful import Resource, abort
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ScrapperCompanyName(Resource):
    def get(self, siren: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        driver = webdriver.Remote(
            command_executor="http://172.18.0.3:4444/wd/hub",
            options=chrome_options,
        )
        driver.get("https://www.societe.com")
        search_form = driver.find_element(By.NAME, "champs")
        search_form.send_keys(siren)
        search_form.submit()

        try:
            company_name = driver.find_element(By.ID, "identite_deno").text
            driver.quit()
            return company_name, 200

        except NoSuchElementException:
            driver.quit()
            abort(404, message=f"Company name with SIREN number: {siren} was not found")
