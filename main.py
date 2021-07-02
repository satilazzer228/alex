import asyncio
import json
import multiprocessing
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import BOT_TOKEN, login, password


def send_message(chat_id, text):  # send telegram message
    try:
        URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
        url = URL + f'sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)
    except Exception as ex:
        pass


def write_file(link, lang, price):  # write to file
    try:
        file = 'Старые.txt'
        with open(file, encoding='utf-8') as f:
            for line in f:
                # check old link
                if str(link) in line:
                    link = ""
                    return False
                    break
            if link and lang == 'Русский' and price != 0:
                # write new link
                f.close()
                with open(file, 'a', encoding='utf-8') as f:
                    f.writelines(str(link) + "\n")
                    return True
    except Exception as ex:
        # send error
        pass


def find_urls(url):
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
        # Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285"
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)  # data of course(json)
    for num in range(0, 16):
        url_of_course = data['unit']['items'][num]['url']
        url_of_course = 'https://www.udemy.com' + url_of_course
        language = data['unit']['items'][num]['locale']['title']
        course_id = data['unit']['items'][num]['id']
        r = requests.get(
            f'https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,recommendation,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,incentives_context,top_companies_notice_context,curated_for_ufb_notice,sidebar_container,purchase_tabs_context,subscribe_team_modal_context,lifetime_access_context',
            headers=headers)
        course_data = json.loads(r.text)  # data of course(json)
        price = course_data['price_text']['data']['pricing_result']['price']['amount']
        result = write_file(url_of_course, language, price)
        if result:
            # course info
            category_id_of_course = data['unit']['recommendation_params']['category_id']
            name = data['unit']['items'][num]['title']
            category_name = data['unit']['items'][num]['context_info']['category']['title']
            name_if_instructor = data['unit']['items'][num]['visible_instructors'][0]['display_name']
            new_course_data = {name: [url_of_course, category_id_of_course, category_name, name_if_instructor]}
            with open('Новые.json', 'r+', encoding='utf-8') as file:
                courses_data = json.load(file)
                courses_data.update(new_course_data)
                file.seek(0)
                json.dump(courses_data, file, indent=4, ensure_ascii=False)
            send_message(1792076176, name)


async def main():
    while True:
        try:
            page_ids = [288, 268, 328, 294, 292, 269, 290, 273, 276, 278]  # page ids
            for page_id in page_ids:
                with multiprocessing.Pool(processes=4) as pool:  # multiprocessing
                    all_pages_list = [
                        f'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={page}&page_size=16&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&sort=newest&category_id={page_id}&source_page=category_page&locale=ru_RU&currency=usd&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat'
                        for page in range(1, 100)]  # page_number index of url
                    pool.map(find_urls, all_pages_list)
                # wait while post
                await post()  # wait while sleep
            await asyncio.sleep(1000)
        except Exception as e:
            pass


async def post():
    try:
        # post
        with open('Новые.json', 'r+', encoding='utf-8') as file:
            courses_data = json.load(file)
        for key, value in courses_data.items():
            try:
                # driver init
                options = webdriver.FirefoxOptions()
                # user-agent
                options.set_preference("general.useragent.override",
                                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                       "like Gecko) Chrome/90.0.4430.212 Safari/537.36")
                headers = {
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
                }
                # disable webdriver mode
                options.set_preference("dom.webdriver.enabled", False)
                driver = webdriver.Firefox(
                    executable_path="C:\\Users\\Admin\\Desktop\\python\\kwork\\Alex888\\geckodriver.exe",
                    options=options
                )
                ###

                # course info
                r = requests.get(value[0], headers=headers)
                soup = BeautifulSoup(r.text, 'lxml')
                desc_list = soup.find(class_="ud-component--course-landing-page-udlite--description").find_all('p')
                ###

                # same dict
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

                # go to site

                driver.get("https://skladchik.com")
                # find sign in
                driver.find_element_by_class_name('concealed').click()
                # login

                driver.find_element_by_name('login').clear()
                driver.find_element_by_name('login').send_keys(login)
                # password

                driver.find_element_by_name('password').clear()
                driver.find_element_by_name('password').send_keys(password + Keys.ENTER)
                time.sleep(5)
                # find same category

                driver.find_element_by_class_name(same_category[str(value[1])]).find_element_by_class_name(
                    'nodeTitle').find_element_by_tag_name('a').click()
                time.sleep(5)
                # make post

                driver.find_element_by_class_name('topCtrl').click()
                time.sleep(5)
                # title of post

                driver.find_element_by_id('ctrl_title_thread_create').clear()
                driver.find_element_by_id('ctrl_title_thread_create').send_keys(key + f" [Udemy] [{value[3]}]")
                # prev_moves

                driver.find_element_by_class_name('redactor_btn_indent').click()
                driver.find_element_by_class_name('redactor_btn_container_undo').click()
                time.sleep(1)

                # make additional configs
                driver.find_element_by_id('XenForoUniq0_tag').send_keys(value[2] + ", " + 'udemy, ' + 'курс')
                time.sleep(1)
                driver.find_element_by_name('share_price').send_keys('999')
                time.sleep(1)
                # driver.find_element_by_name('share_fixed_contrib').click()
                time.sleep(1)
                # driver.find_element_by_id('ctrl_locked_organize').click()
                time.sleep(1)
                # desc of post and next frame
                driver.switch_to.frame(driver.find_element_by_class_name('redactor_textCtrl'))
                driver.find_element_by_tag_name('body').clear()
                time.sleep(3)
                desc = ''.join(f"{sym.text}\n" for sym in desc_list)
                driver.find_element_by_tag_name('body').send_keys(
                    key + "\n\n" + "Описание" + "\n\n" + desc + "\n\n" + value[0] + Keys.ENTER)
                time.sleep(5)
            except Exception as ex:
                # send error
                send_message(1792076176, 'ошибка')
            finally:
                driver.close()
                driver.quit()

        # rewrite
        with open('Новые.json', 'w', encoding='utf-8') as file:
            courses_data = {k: v for k, v in courses_data.items() if k == 0 and v == 0}
            json.dump(courses_data, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        # send error
        pass


if __name__ == '__main__':
    # run program
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
