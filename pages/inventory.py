from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from checking.checking import Checking


class Inventory_Page:
    """ Класс для работы со страницей товаров"""

    page_url = 'https://www.saucedemo.com/inventory.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver


    def get_products(self):
        """ получение списка товаров со страницы"""

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        products_elements_list = self.driver.find_elements(By.CLASS_NAME, 'inventory_item')
        products_list = list()  # пустой список, который будем заполнять результатами
        for product_node in products_elements_list:
            product_name = product_node.find_element(By.XPATH, './/div[@class="inventory_item_name "]').text
            product_price = product_node.find_element(By.XPATH, './/div[@class="inventory_item_price"]').text
            product_add_to_cart_button = product_node.find_element(By.CLASS_NAME, 'btn_inventory')
            product_add_to_cart_button_id = product_add_to_cart_button.get_attribute('id')
            product_item = {
                'name': product_name,
                'price': product_price,
                'add_to_card_button_id': product_add_to_cart_button_id
            }
            products_list.append(product_item)

        assert len(products_list) > 0, 'Ошибка, нулевое количество товаров на странице!'

        print(f"[Страница товаров {self.page_url}]: Успешно считано {len(products_list)} товаров.\n")

        return products_list


    def add_to_card(self, add_to_card_button_id_):
        """ метод добавления товара в корзину
            на входе id кнопки товара, на которую должен нажать скрипт
            """
        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        if not add_to_card_button_id_:
            print(f'Невозможно добавить товар в корзину, указан пустой id товара')
            return

        try:
            add_to_cart_btn = self.driver.find_element(By.ID, add_to_card_button_id_)
            add_to_cart_btn.click()
            print(f'[Добавление в корзину] Нажата кнопка товара с id={add_to_card_button_id_}')
        except NoSuchElementException as err:
            print(f'[Добавление в корзину] Ошибка нажатия на кнопку товара id={add_to_card_button_id_}. Текст '
                  f'ошибки:\n{err}')


    def goto_cart(self):
        """ Клик на корзину (переход на страницу cart.html)"""
        if Checking.check_wrong_page(self.driver, self.page_url):
            return
        cart_button = self.driver.find_element(By.XPATH, '//a[@class="shopping_cart_link"]')
        cart_button.click()
        print(f"[Переход в корзину] Нажата кнопка Корзина")
