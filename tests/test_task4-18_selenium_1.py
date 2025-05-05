from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from random import randint
import time

from conftest import driver

# импорт модулей отдельных страниц проекта
from pages.home import HomePage
from pages.inventory import Inventory_Page
from pages.cart import Cart_Page
from pages.checkout_step_one import Checkout_step_one_Page
from pages.checkout_step_two import Checkout_step_two_Page
from pages.checkout_complete import Checkout_complete_Page
from checking.checking import Checking

# собираем URL страниц из модулей отдельных страниц
home_url = HomePage.page_url
inventory_url = Inventory_Page.page_url
cart_url = Cart_Page.page_url
checkout_step_one_url = Checkout_step_one_Page.page_url
checkout_step_two_url = Checkout_step_two_Page.page_url
checkout_complete_url = Checkout_complete_Page.page_url


def get_random_numbers(count, maxnum):
    """ возвращаем count случайных неповторяющихся целых чисел между 0 и maxnum
        применение: выбрать X разных элементов какого-то списка
    """
    random_numbers_list = list()
    if count < 0 or count > maxnum or maxnum < 0:
        return random_numbers_list

    while len(random_numbers_list) < count:
        random_num = randint(0, maxnum)
        if random_num not in random_numbers_list:
            random_numbers_list.append(random_num)

    return random_numbers_list


def test_smoke(driver):
    """ основной код смоук-текст сайта
        driver - функция-фикстура из conftest.py
    """

    homepage = HomePage(driver)
    inventory_page = Inventory_Page(driver)
    cart_page = Cart_Page(driver)
    checkout_step_one_page = Checkout_step_one_Page(driver)
    checkout_step_two_page = Checkout_step_two_Page(driver)
    checkout_complete_page = Checkout_complete_Page(driver)

    homepage.open()
    Checking.check_url_change(driver, initial_url=home_url, expected_url=home_url, timeout=0)
    time.sleep(0)

    homepage.click_login()
    homepage.check_login_error()
    time.sleep(0)

    Checking.check_url_change(driver, initial_url=home_url, expected_url=inventory_url, timeout=1)


    products_list = inventory_page.get_products()
    print('Список товаров на странице:')
    for i, product_item in enumerate(products_list, start=0):
        print(f"Товар #{i}: {product_item['name']}, цена {product_item['price']}")

    product_random_indexes = get_random_numbers(2, len(products_list)-1)
    print(f"\nВыбраны следующие случайные номера товаров для добавления в корзину (начиная с 0):"
          f" {product_random_indexes}\n")

    products_list_cart = list()  # итоговый список товаров, добавляемых в корзину
    products_summ = 0  # цена всех товаров

    for index in product_random_indexes:
        product = products_list[index]
        products_list_cart.append(product)  # с этим списком потом будем сверять содержимое корзины
        product_add_to_card_button_id = product['add_to_card_button_id']
        print(f"[Добавление в корзину] Добавляем товар #{index}: {product['name']}, {product['price']}")
        product_price = float(product['price'].replace('$',''))
        products_summ += product_price
        # клик на кнопке "Add to card" для каждого товара
        inventory_page.add_to_card(product_add_to_card_button_id)
    print(f'[Добавление в корзину] В корзину отправлено {len(products_list_cart)} товаров на сумму ${products_summ}')

    inventory_page.goto_cart()
    Checking.check_url_change(driver, initial_url=inventory_url, expected_url=cart_url, timeout=1)

    cart_products_list = cart_page.get_cart_products()
    # cart_products_list[0]['name'] = 'empty name'  # проверка поврежденных данных корзины

    Checking.compare_cart_with_selected_products(products_list_cart, cart_products_list)

    cart_page.goto_checkout()
    Checking.check_url_change(driver, initial_url=cart_url, expected_url=checkout_step_one_url, timeout=1)

    first_name = 'John'
    last_name = 'Dow'
    zip_postal_code = '111222333'

    checkout_step_one_page.fill_user_information(first_name, last_name, zip_postal_code)
    Checking.check_url_change(driver, initial_url=checkout_step_one_url, expected_url=checkout_step_two_url, timeout=1)

    checkout_product_list = checkout_step_two_page.get_checkout_products()
    Checking.compare_cart_with_selected_products(checkout_product_list, cart_products_list)

    checkout_price = checkout_step_two_page.get_checkout_price_notaxes()  # + 100 для проверки ассерта
    Checking.compare_summ_cart_with_summ_checkout(products_summ, checkout_price)

    checkout_step_two_page.click_finish()
    Checking.check_url_change(driver, initial_url=checkout_step_two_url, expected_url=checkout_complete_url, timeout=1)

    print(f'Smoke-тест для {HomePage.page_url} пройден!')

