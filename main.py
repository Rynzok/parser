from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def create_dict(x, y):
    result_dict = {}
    # print('dfgh')
    for j in range(min(len(x), len(y))):
        key = code[j].text
        value = description[j].text
        result_dict[key] = value
    return result_dict


def create_dict2(elements):
    # print('create_dict2')
    result_dict = {}

    # Проходим по элементам с шагом 2
    for el in elements:
        parts = el.text.split('\n')

        # Проверяем, что в строке есть хотя бы два элемента
        if len(parts) >= 2:
            key = parts[0].strip()
            value = parts[1].strip()
            result_dict[key] = value

    return result_dict

def clic_click(click_element, id):
    click_element.click()
    # print("clic_click")
    # time.sleep(1)
    key = driver.find_elements(By.CLASS_NAME,'mpk_table_list')
    href = driver.find_elements(By.CSS_SELECTOR, 'a.mktu-category__class-link.blue-link')
    length = len(href)
    print('length: '+ str(length))
    if key :
        print(create_dict2(key))
        for j in range(length):
            print('j: ' + str(j))
            href = driver.find_elements(By.CSS_SELECTOR, 'a.mktu-category__class-link.blue-link')
            clic_click(href[j], j)
        driver.back()

    elif driver.find_elements(By.CLASS_NAME, 'mktu-class__content'):
        data = driver.find_element(By.CLASS_NAME, 'mktu-class__content').text
        result_dict = {}
        for line in data.strip().split('\n'):
            key, value = line.split(' - ', 1)
            result_dict[key] = value.strip()
        print(result_dict)
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

    all_dict = create_dict(code, description)

    print(all_dict)

    first_length = len(code)
    print(first_length)
    for i in range(first_length):
        time.sleep(1)
        code2 = driver.find_elements(By.CLASS_NAME, 'mktu-category__class-link')
        print('INDEX: ' + str(i) + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        clic_click(code2[i], i)


except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()  # Закрыть браузер

# освободите ресурсы, выделенные Selenium, и выключите браузер.
driver.quit()