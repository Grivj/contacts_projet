import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

SIREN = "838170918"

# ready = False
# while not ready:
#     try:
#         request = requests.get("http://localhost:4444/status", timeout=1)
#         print(request)
#         if request.status_code == 200:
#
#             ready = True
#     except ConnectionResetError or ConnectionError:
#         continue


def get_company_name(remote_url: str, siren: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Remote(
        command_executor=f"{remote_url}/wd/hub",
        options=chrome_options,
    )
    driver.get("https://www.societe.com")
    search_form = driver.find_element(By.NAME, "champs")
    search_form.send_keys(siren)
    search_form.submit()
    company_name = driver.find_element(By.ID, "identite_deno")

    print(company_name.text)
    driver.quit()
