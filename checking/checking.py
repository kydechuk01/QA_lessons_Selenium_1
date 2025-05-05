from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Checking:
    """ Класс с методами проверок"""

    @staticmethod
    def check_url_change(driver: WebDriver, initial_url: str, expected_url: str, timeout=3):
        """ Проверка:
            а) нахождения на странице (когда оба параметра url совпадают)
            ИЛИ
            б) проверка смены страницы на ожидаемую"""

        # проверка, что мы УЖЕ находимся на заданной странице, когда на вход поданы одинаковые значения
        if expected_url == initial_url:
            assert driver.current_url == expected_url, f'Ожидаемый URL={expected_url}, ' \
                                                       f'отличается от текущего: {driver.current_url}'
            print(f'[Проверка URL] Текущий URL соответствует ожидаемому ({expected_url})')
            return True

        # Устанавливаем ожидание события "Изменение URL с первоначального на другой"
        # Выход из ожидания: Смена адреса ИЛИ истечение timeout секунд
        try:
            WebDriverWait(driver, timeout).until(EC.url_changes(initial_url))
        except TimeoutException:
            pass

        assert driver.current_url == expected_url, f'Ожидаемый URL={expected_url}, отличается от текущего: ' \
                                                   f' {driver.current_url}'
        print(f'\n[Проверка URL] URL успешно изменился и соответствует ожидаемому значениию ({expected_url})\n')
        return True


    @staticmethod
    def check_wrong_page(driver: WebDriver, page_url, method_name=''):
        """ Проверка, чтобы методы различных страниц нельзя было вызывать с других страниц"""
        if driver.current_url != page_url:
            if method_name != '':
                method_name = f'[{method_name}] '  # если метод указан, обернем его в скобки и добавим пробел
            print(f"Вызов метода {method_name}страницы {page_url} с другой страницы ({driver.current_url})!")
            return True
        else:
            return False


    @staticmethod
    def compare_cart_with_selected_products(product_list, cart_list):
        """ метод сравнения списков товаров, добавленных в корзину, с содержимым корзины на следующей странице"""

        # удаляем лишнее поле данных из списка продуктов
        for item in product_list:
            if 'add_to_card_button_id' in item:
                del item['add_to_card_button_id']

        # сортируем списки перед сравнением
        sorted_products_list = sorted(product_list, key=lambda x: x['name'])
        sorted_cart_list = sorted(cart_list, key=lambda x: x['name'])

        assert sorted_cart_list == sorted_products_list, 'Список в корзине не совпал со списком помещенных в нее ' \
                                                         'товаров!'

        print('[Сравнение списков] Список товаров в корзине совпал с выбранными ранее товарами')
        return True


    @staticmethod
    def compare_summ_cart_with_summ_checkout(sum1, sum2):
        """ Сравнение сумм корзины и счета"""
        assert float(sum1) == float(sum2), f'[Сравнение сумм] Значение суммы товаров, добавленных в корзину ({sum1}) ' \
                                           f'не совпадает с суммой ({sum2}) на странице оплаты, этап 2.'
        print(f'[Cравнение сумм] Суммы товаров в корзине ({sum1}) совпадает с суммой счета.')
        return True



















