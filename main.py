import time  # Импортируем модуль time для использования функции задержки
from selenium import webdriver  # Импортируем модуль webdriver из пакета selenium для управления браузером
from selenium.webdriver.common.by import By  # Импортируем класс By для указания методов поиска элементов на странице
from selenium.webdriver.common.keys import Keys  # Импортируем класс Keys для имитации нажатий клавиш на клавиатуре
from selenium.webdriver.chrome.service import Service  # Импортируем класс Service для управления службой ChromeDriver


def start_driver():
    # Укажите путь к вашему файлу chromedriver
    path = 'C:/WebDriver/bin/chromedriver.exe'

    # Создайте экземпляр сервиса для chromedriver
    service = Service(path)

    # Создайте экземпляр опций для браузера Chrome
    options = webdriver.ChromeOptions()
    # Добавьте опцию для запуска браузера в фоновом режиме (без графического интерфейса)
    options.add_argument('--headless')
    # Добавьте опцию для отключения использования GPU
    options.add_argument('--disable-gpu')
    # Создайте экземпляр браузера Chrome с указанием сервиса и опций
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def search_wikipedia(driver, query):
    # Перейти на главную страницу Wikipedia
    driver.get("https://www.wikipedia.org/")
    # Найти поле поиска на странице по имени атрибута (NAME)
    search_box = driver.find_element(By.NAME, "search")
    # Ввести поисковый запрос в поле поиска
    search_box.send_keys(query)
    # Нажать клавишу "Enter" для выполнения поиска
    search_box.send_keys(Keys.RETURN)
    # Подождать 2 секунды для полной загрузки страницы результатов поиска
    time.sleep(2)


def list_paragraphs(driver):
    # Найти все абзацы на странице по CSS-селектору "p"
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    # Перебрать и вывести текст каждого абзаца
    for i, paragraph in enumerate(paragraphs):
        print(f"Paragraph {i + 1}: {paragraph.text}")


def list_links(driver):
    # Найти все ссылки в основном контенте страницы по CSS-селектору "#bodyContent a"
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    # Перебрать и вывести текст и URL каждой ссылки
    for i, link in enumerate(links):
        print(f"{i + 1}: {link.text} - {link.get_attribute('href')}")
    return links


def navigate_to_link(driver, link_index, links):
    # Перейти по выбранной ссылке по её индексу
    links[link_index].click()
    # Подождать 2 секунды для полной загрузки новой страницы
    time.sleep(2)


def main():
    # Запустить браузер с использованием функции start_driver
    driver = start_driver()
    # Запросить у пользователя ввод первоначального поискового запроса
    initial_query = input("Введите первоначальный запрос: ")
    # Выполнить поиск в Wikipedia по введённому запросу
    search_wikipedia(driver, initial_query)

    while True:
        # Запросить у пользователя выбор действия
        action = input(
            "Выберите действие:\n1 - Листать параграфы текущей статьи\n2 - Перейти на одну из связанных страниц\n3 - "
            "Выйти из программы\n")

        if action == "1":
            # Вывести все абзацы текущей статьи
            list_paragraphs(driver)
        elif action == "2":
            # Вывести все ссылки текущей статьи
            links = list_links(driver)
            if links:
                # Запросить у пользователя выбор ссылки для перехода
                link_index = int(input(f"Введите номер ссылки для перехода (1-{len(links)}): ")) - 1
                if 0 <= link_index < len(links):
                    # Перейти по выбранной ссылке
                    navigate_to_link(driver, link_index, links)
                else:
                    print("Неверный номер ссылки.")
            else:
                print("Нет доступных ссылок.")
        elif action == "3":
            # Закрыть браузер и выйти из программы
            driver.quit()
            break
        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")


if __name__ == "__main__":
    main()  # Запустить основную функцию программы
