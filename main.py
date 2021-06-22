import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import multiprocessing
from config import BOT_TOKEN, login, password
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pickle

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")

# options.headless = True


# cookies
driver = webdriver.Chrome(
    executable_path="C:\\Users\\Admin\\Desktop\\python\\kwork\\Alex888\\chromedriver.exe",
    options=options
)

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
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285"
        "user-agent": f"{useragent.random}"
    }
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    for num in range(0, 16):
        name = data['unit']['items'][num]['title']
        url_of_course = data['unit']['items'][num]['url']
        url_of_course = 'https://www.udemy.com' + url_of_course
        result = write_file(url_of_course, 'Старые')
        category_id_of_course = data['unit']['recommendation_params']['category_id']
        if result:
            '''r = requests.get(url_of_course, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            description = soup.find(class_="show-more--content--isg5c show-more--with-gradient--2abmN").text
            same_category = {
                '288': 'node_21',
                '268': 'node_24',
                '328': 'node_103',
                '294': 'node_16',
                '292': 'node_38',
                '269': 'node_19',
                '290': 'node_102',
                '273': 'node_78',
                '276': 'node_71',
                '278': 'node_60'
            }
            driver.get('https://skladchik.com')
            time.sleep(1)
            # sign in
            driver.find_element_by_class_name('concealed').click()
            time.sleep(1)
            driver.find_element_by_name('login').send_keys(login)
            time.sleep(1)
            driver.find_element_by_name('password').send_keys(password)
            time.sleep(1)
            driver.find_element_by_class_name('button').click()
            time.sleep(1)
            # pickle.dump(driver.get_cookies(), open(f"{login}_cookies", "wb"))
            driver.find_element_by_class_name(same_category[category_id_of_course]).find_element_by_class_name('nodeTitle').click()
            time.sleep(5)
            driver.find_element_by_class_name('linkGroup').click()
            time.sleep(5)
            driver.find_element_by_class_name('textCtrl titleCtrl').send_keys(name + '.' + ' [Вячеслав Казанков]')
            time.sleep(5)
            driver.find_element_by_class_name(
                'redactor_textCtrl redactor_MessageEditor redactor_BbCodeWysiwygEditor redactor_').send_keys(
                description)'''
            pass


if __name__ == '__main__':
    while True:
        try:
            page_ids = [288, 268, 328, 294, 292, 269, 290, 273, 276, 278]
            for page_id in page_ids:
                with multiprocessing.Pool(processes=8) as pool:
                    all_pages_list = [
                        f'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={page}&page_size=16&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&category_id={page_id}&source_page=category_page&locale=ru_RU&currency=usd&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat'
                        for page in range(1, 100)]
                    pool.map(find_urls, all_pages_list)
            time.sleep(secs)
        except Exception as e:
            print(e)
