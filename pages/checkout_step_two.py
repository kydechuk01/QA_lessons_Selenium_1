from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from checking.checking import Checking


class Checkout_step_two_Page:

    page_url = 'https://www.saucedemo.com/checkout-step-two.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver


    def click_finish(self):
        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        button_finish = self.driver.find_element(By.XPATH, '//button[@id="finish"]')
        button_finish.click()
        print(f'[Кнопка] Нажата кнопка Finish')


    def get_checkout_products(self):
        """ получение списка товаров со страницы"""

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        checkout_overview_list = self.driver.find_elements(By.XPATH, '//div[@class="cart_item"]')
        checkout_products_list = list()  # пустой список, который будем заполнять результатами
        for checkout_node in checkout_overview_list:
            product_name = checkout_node.find_element(By.XPATH, './/div[@class="inventory_item_name"]').text
            product_price = checkout_node.find_element(By.XPATH, './/div[@class="inventory_item_price"]').text
            product_item = {
                'name': product_name,
                'price': product_price,
            }
            checkout_products_list.append(product_item)

        assert len(checkout_products_list) > 0, 'Ошибка, нулевое количество товаров в корзине!'

        print(f"[Страница оплаты, этап 2, сверка данных {self.page_url}]: "
              f"Успешно считано {len(checkout_products_list)} товаров:\n"
              f"{checkout_products_list}")

        return checkout_products_list


    def get_checkout_price_notaxes(self):
        """ Вытаскиваем со страницы значение суммы корзины до налогов, которое предлагает сайт """

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        checkout_price_locator = self.driver.find_element(By.CLASS_NAME, 'summary_subtotal_label')
        checkout_price = checkout_price_locator.text
        print(f'[Страница оплаты, этап 2] Считана общая сумма счета без налогов: {checkout_price}')
        checkout_price = checkout_price.split('$')[-1]  # убираем все до знака $ включительно
        return float(checkout_price)
