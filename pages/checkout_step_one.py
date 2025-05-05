import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from checking.checking import Checking


class Checkout_step_one_Page:

    page_url = 'https://www.saucedemo.com/checkout-step-one.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver


    def fill_user_information(self, first, last, zip_code):
        """ заполнение полей данными """
        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        firstname_locator = self.driver.find_element(By.ID, 'first-name')
        lastname_locator = self.driver.find_element(By.ID, 'last-name')
        zip_code_locator = self.driver.find_element(By.ID, 'postal-code')

        firstname_locator.send_keys(first)
        lastname_locator.send_keys(last)
        zip_code_locator.send_keys(zip_code)

        print(f'[Страница оплаты, этап 1, ввод данных {self.page_url}] Введены значения: {first}, {last}, {zip_code}')
        time.sleep(1)

        continue_button = self.driver.find_element(By.ID, 'continue')
        continue_button.click()
        print(f'[Кнопка] Нажата кнопка Continue')