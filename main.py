import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import multiprocessing
from config import BOT_TOKEN

'''# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")
# headless mode
# options.add_argument("--headless")


driver = webdriver.Chrome(
    executable_path="C:\\Users\\Admin\\Desktop\\python\\kwork\\Alex888\\chromedriver.exe",
    options=options
)'''

chatID = '1792076176'  # ID telegram получателя
secs = 10  # Интервал проверок в секундах


def send_message(chat_id, text):
    URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
    url = URL + f'sendMessage?chat_id={chat_id}&text={text}'
    requests.get(url)


def write_file(link, file):
    file = file + '.txt'
    with open(file, encoding='utf-8') as f:
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
    data = r.json()
    for num in range(0, 16):
        name = data['unit']['items'][num]['title']
        url_of_course = data['unit']['items'][num]['url']
        url_of_course = 'https://www.udemy.com' + url_of_course
        result = write_file(url_of_course, 'Старые')
        if result:
            send_message(chatID, str(name) + '\n' + str(url_of_course))
        print(name, url_of_course)


if __name__ == '__main__':
    while True:
        with multiprocessing.Pool(processes=10) as pool:
            page_ids = [269, 288, 328, 294, 292, 296, 290, 274, 273, 276, 278, 300]
            try:
                pool.map(find_urls, [
                    f'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={page}&page_size=60&subcategory=&instructional_level=&lang=ru&price=&duration=&closed_captions=&sort=popularity&category_id=269&source_page=category_page&locale=ru_RU&currency=usd&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat'
                    for page in range(1, 100)])
            except Exception as e:
                print(e)
        time.sleep(secs)
