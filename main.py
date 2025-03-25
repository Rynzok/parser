from selenium import webdriver
from selenium.webdriver.common.by import By
from db_connection import insert_first_list_in_db, insert_second_list_in_db
import time


def create_list_of_tuples(x, y):
    result_list = []
    for j in range(min(len(x), len(y))):
        key = x[j].text  # Используем x для ключа
        value = y[j].text  # Используем y для значения
        result_list.append((key, value))  # Добавляем кортеж (key, value) в список
    return result_list


def create_list_of_lists(elements, index):
    result_list = []

    # Проходим по элементам
    for el in elements:
        parts = el.text.split('\n')

        # Проверяем, что в строке есть хотя бы два элемента
        if len(parts) >= 2:
            key = parts[0].strip()
            value = parts[1].strip()
            # Добавляем список из key, value и id
            result_list.append([key, value, index])  # Используем index как id

    return result_list

def parse_data_to_list(data, fkey):
    result_list = []
    for line in data.strip().split('\n'):
        key, value = line.split(' - ', 1)  # Разделяем строку на ключ и значение
        result_list.append([key, value.strip(), fkey])  # Убираем лишние пробелы и добавляем в словарь
    return result_list

def clic_click(ref_name, click_element, element_id):
    t_name = click_element.text
    click_element.click()
    # print("clic_click")
    # time.sleep(1)
    key = driver.find_elements(By.CLASS_NAME,'mpk_table_list')
    href = driver.find_elements(By.CSS_SELECTOR, 'a.mktu-category__class-link.blue-link')
    length = len(href)
    print('length: '+ str(length))
    if key :
        result_list = create_list_of_lists(key, id)
        insert_second_list_in_db(result_list, t_name, ref_name)
        for j in range(length):
            print('j: ' + str(j))
            href = driver.find_elements(By.CSS_SELECTOR, 'a.mktu-category__class-link.blue-link')

            clic_click(href[j].text ,href[j], j + 1, )
        driver.back()

    elif driver.find_elements(By.CLASS_NAME, 'mktu-class__content'):
        data = driver.find_element(By.CLASS_NAME, 'mktu-class__content').text
        result_list = parse_data_to_list(data, element_id)
        insert_second_list_in_db(result_list, t_name, ref_name)
        driver.back()
    else:
        driver.back()

    return


# инициализируем экземпляр драйвера хрома (браузера)
driver = webdriver.Chrome()

# посетите целевой сайт
driver.get('https://prilan.ru/eskd/')


# Найдите элемент по классу и получите текст
try:
    time.sleep(1)
    code = driver.find_elements(By.CLASS_NAME, 'mktu-category__class-link')
    description = driver.find_elements(By.CLASS_NAME, 'mktu-category__class-discr')
    # Создание словаря

    all_list = create_list_of_tuples(code, description)
    insert_first_list_in_db(all_list)


    # print(all_list)
    table_name = 'main'

    first_length = len(code)
    print(first_length)

    for i in range(first_length):
        time.sleep(1)
        code2 = driver.find_elements(By.CLASS_NAME, 'mktu-category__class-link')
        print('INDEX: ' + str(i) + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        clic_click(table_name, code2[i], i + 1)


except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()  # Закрыть браузер

# освободите ресурсы, выделенные Selenium, и выключите браузер.
driver.quit()