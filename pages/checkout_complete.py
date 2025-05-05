from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class Checkout_complete_Page:

    page_url = 'https://www.saucedemo.com/checkout-complete.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver