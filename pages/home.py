from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from checking.checking import Checking


class HomePage:
    """ Класс для работы с начальной страницей (логин)"""

    page_url = 'https://www.saucedemo.com/'

    def __init__(self, driver: WebDriver):
        self.driver = driver


    def open(self):
        self.driver.get(self.page_url)


    def click_login(self):
        """ Ввод логина, пароля и нажатие кнопки Логин"""

        if Checking.check_wrong_page(self.driver, self.page_url):
            return

        test_username = 'standard_user'
        test_password = 'secret_sauce'
        # test_username, test_password = 'abc', ''
        input_username = self.driver.find_element(By.ID, "user-name")
        input_password = self.driver.find_element(By.ID, "password")
        btn_login = self.driver.find_element(By.ID, "login-button")
        input_username.send_keys(test_username)
        input_password.send_keys(test_password)
        print(f'[Ввод данных] Введены логин и пароль: {test_username}, pass={test_password}')
        btn_login.click()
        print(f'[Кнопка] Нажата кнопка: Логин')


    def check_login_error(self):
        """ проверка ошибок, связанных с неверным логином"""

        if Checking.check_wrong_page(self.driver, self.page_url, 'проверка ошибок логина'):
            return

        err_messages = ['Epic sadface: Username and password do not match any user in this service',
                        'Epic sadface: Password is required',
                        'Epic sadface: Username is required']

        error_place_xpath = '//h3[@data-test="error"]'
        login_error_msg = self.driver.find_element(By.XPATH, error_place_xpath)
        login_error_msg_text = login_error_msg.text
        if login_error_msg_text in err_messages:
            assert False, f'Ошибка логина: {login_error_msg_text}'
        else:
            print("[Вход в систему] Ошибок логина не обнаружено")
