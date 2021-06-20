import time
import requests
import json
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import multiprocessing

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
options.headless = True

driver = webdriver.Chrome(
    executable_path=r"C:\Users\Admin\Desktop\python\kwork\Alex888\chromedriver.exe",
    options=options
)

chatID = '1792076176'  # ID telegram получателя
secs = 10  # Интервал проверок в секундах


def send_message(chat_id, text):
    URL = 'https://api.telegram.org/bot' + '704235611:AAHHODJ4rBdwPEMS2rRr4NHnLNDdDJ99Yd8' + '/'
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url, timeout=5.0)


def write_file(link, file):
    file = file + '.txt'
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if str(link) in line:
                link = ""
                return False
                break
        if link:
            f.close()
            with open(file, 'a', encoding='utf-8') as f:
                f.writelines(str(link) + "\n")
                return True


def find_urls(url):
    r = requests.get(url)
    data = json.loads(r.text)
    for num in range(0, 15):
        name = data['unit']['items'][num]['title']
        url_of_course = data['unit']['items'][num]['url']
        url_of_course = 'https://www.udemy.com' + url_of_course
        result = write_file(url_of_course, 'Старые')
        if (result):
            send_message(chatID, str(name) + '\n' + str(url_of_course))
        print(name, url_of_course)


if __name__ == '__main__':
    while True:
        with multiprocessing.Pool(10) as pool:
            page_ids = [269, 288, 328, 294, 292, 296, 290, 274, 273, 276, 278, 300]
            try:
                pool.map(find_urls, [
                    f'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={page}&page_size=60&subcategory=&instructional_level=&lang=ru&price=&duration=&closed_captions=&sort=popularity&category_id=269&source_page=category_page&locale=ru_RU&currency=usd&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat'
                    for page in range(1, 100)])
            except Exception as e:
                pool.close()
        time.sleep(secs)
