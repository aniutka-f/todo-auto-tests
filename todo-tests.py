from selenium.webdriver.common.by import By
import pytest

link = "https://lovely-genie-b5af1b.netlify.app/"


def create_todo(browser, type_todo):
    browser.get(link)

    input_text_todo = browser.find_element(By.CSS_SELECTOR, '[data-testid="input_content"]')
    button_add_todo = browser.find_element(By.CSS_SELECTOR, '[data-testid="add_todo"]')
    radio_type_todo = browser.find_element(By.XPATH, '//div[@class="options"]//span[@class="bubble ' + type_todo + '"]')

    init_todo_text = "type = " + type_todo

    def is_disabled_button():
        return button_add_todo.get_attribute("disabled")  # True or False

    if not is_disabled_button():
        print("button isnt disabled")

    input_text_todo.send_keys(init_todo_text)

    if not is_disabled_button():
        print("button isnt disabled")

    radio_type_todo.click()

    if is_disabled_button():
        print("button disabled")

    button_add_todo.click()

    # проверяем что текст в туду соответствует заведенному
    text_todo = browser.find_element(By.XPATH, '//section[@class="space-column"]//input[@class="todo-content"]')
    check_type = browser.find_element(By.XPATH, '//section[@class="space-column"]//span')

    text_todo_value = text_todo.get_attribute("value")

    if not text_todo_value == init_todo_text:
        print("Текст в туду не соответсвует заведенному")

    # Проверияем, что тип туду соответсвует заведенному
    check_type_class = check_type.get_attribute('class')
    type_point = bool(check_type_class.find(type_todo))
    if not type_point:
        print('Неверный тип туду')


def create_todo_without_check(browser):  # Создаем туду без дополнительных проверок
    input_text_todo = browser.find_element(By.CSS_SELECTOR, '[data-testid="input_content"]')
    input_text_todo.send_keys("111")
    radio_type_todo = browser.find_element(By.XPATH, '//div[@class="options"]//span')
    radio_type_todo.click()
    button_add = browser.find_element(By.CSS_SELECTOR, '[data-testid="add_todo"]')
    button_add.click()


def check_missing_buttons(browser):  # Проверка отсутствия кнопок Clear all & Hide
    button_clear_all = browser.find_elements(By.CSS_SELECTOR, '[data-testid="clear_all"]')
    button_hide = browser.find_elements(By.CSS_SELECTOR, '[data-testid="change_visible"]')

    if button_clear_all or button_hide:
        print("Присутствует ненужная кнопка")


def empty_list(browser):  # Проверка пустой ли список
    empty_pounts = browser.find_elements(By.CSS_SELECTOR, '[class="todo-item"]')
    if empty_pounts:
        print("Ненужные туду есть на странице")


def editing(browser):  # редактируем и проверка редактирования
    input_editing = browser.find_element(By.XPATH, "//section[@class='space-column']//input[@type='text']")
    input_editing_text = input_editing.get_attribute("value")
    input_editing.click()
    input_editing.send_keys("editing")
    value_ed = input_editing_text + "editing"
    input_editing_1 = browser.find_element(By.XPATH, "//section[@class='space-column']//input[@type='text']")
    input_editing_text_1 = input_editing_1.get_attribute("value")
    if value_ed not in input_editing_text_1:
        print("неверный текст после редактирования")


@pytest.mark.smoke
class TestMain:
    def test_init(self, browser):

        check_missing_buttons(browser)  # проверка, что нет кнопок
        empty_list(browser)  # проверка, что нет элементов туду на странице
        create_todo(browser, 'default')  # создаем туду пункты

        editing(browser)  # редактируем и проверка редактирования
        input_text_todo = browser.find_element(By.XPATH,
                                               "//section[@class='space-column']//span")  # делаем туду выполненым
        input_text_todo.click()

        browser.find_element(By.CSS_SELECTOR, '[data-testid = "delete"]').click()  # удалить пункт туду

        create_todo(browser, 'default')  # создать дополнительные туду пункты
        create_todo(browser, 'private')  # создать дополнительные туду пункты

        # Проверка названия кнопки Hide
        button_hide = browser.find_element(By.CSS_SELECTOR, '[data-testid="change_visible"]')
        str_hide_text = button_hide.text
        if "Hide" not in str_hide_text:
            print('Неверное название кнопки Hide')

        button_hide.click()  # Нажать на Hide

        create_todo_without_check(browser)  # Создаем новый туду без проверок

        point_todos = browser.find_elements(By.CSS_SELECTOR, '[class="todo-item"]')  # Проверка, что пунктов туду нет
        if not point_todos:
            print("Элементы отсутствуют на странице")

        str_hide = button_hide.text  # Проверка названия кнопки Show
        if "Show" not in str_hide:
            print("Неверное название кнопки Show")

        button_hide.click()  # нажимаем на Show и проверяем, что элементы отобразились
        browser.find_element(By.CSS_SELECTOR, '[class="todo-item"]')

        # кнопка задизейблена до ввода текста (выбран тип)
        radio_type_todo = browser.find_element(By.XPATH, '//div[@class="options"]//span')
        radio_type_todo.click()
        button_add = browser.find_element(By.CSS_SELECTOR, '[data-testid="add_todo"]')
        is_button_disabled = button_add.get_attribute("disabled")
        if not is_button_disabled:
            print("Кнопка не задезейблена")

        create_todo(browser, 'default')  # создать дополнительный туду

        clear_all = browser.find_element(By.CSS_SELECTOR, '[data-testid="clear_all"]')  # нажать на кнопку clear all
        str_clear = clear_all.text
        if "Clear all" not in str_clear:
            print("Неверное название кнопки Clear all")
        clear_all.click()

        empty_list(browser)  # проверить, что нет элементов после удаления
        check_missing_buttons(browser)
