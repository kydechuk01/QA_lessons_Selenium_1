from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from checking.checking import Checking


class Cart_Page:

    page_url = 'https://www.saucedemo.com/cart.html'

    def __init__(self, driver: WebDriver):
        self.driver = driver


    def get_cart_products(self):
        """ получение списка товаров со страницы"""

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        cart_elements_list = self.driver.find_elements(By.XPATH, '//div[@class="cart_item"]')
        cart_products_list = list()  # пустой список, который будем заполнять результатами
        for cart_node in cart_elements_list:
            product_name = cart_node.find_element(By.XPATH, './/div[@class="inventory_item_name"]').text
            product_price = cart_node.find_element(By.XPATH, './/div[@class="inventory_item_price"]').text
            product_item = {
                'name': product_name,
                'price': product_price,
            }
            cart_products_list.append(product_item)

        assert len(cart_products_list) > 0, 'Ошибка, нулевое количество товаров в корзине!'

        print(f"[Корзина {self.page_url}]: "
              f"Успешно считано {len(cart_products_list)} товаров:\n"
              f"{cart_products_list}")

        return cart_products_list


    def goto_checkout(self):
        """ Нажатие на кнопку Checkout, переход к следующему этапу"""

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        checkout_button = self.driver.find_element(By.CLASS_NAME, 'checkout_button')
        checkout_button.click()
        print(f'[Кнопка] Нажата кнопка Checkout')



