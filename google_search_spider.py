from selenium import webdriver
import time
from pyquery import PyQuery as pq
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


browser = webdriver.Chrome(executable_path=r'D:\Program Files\Python\Python36\Scripts\chromedriver.exe')
browser.get('https://www.google.com')
time.sleep(3)


def search():
    print('正在搜索')
    element = browser.find_element_by_class_name('gLFyf')
    element.send_keys(keyword)
    element.submit()
    time.sleep(3)

    get_info()


def get_info():
    html = browser.page_source
    doc = pq(html)
    items = doc('#search .g .tF2Cxc').items()
    for item in items:
        infos = {
            'title': item.find('.LC20lb').text(),
            'link': item.find('a').attr('href'),
        }
        print(infos)
        # save_to_mongo(infos)
        time.sleep(1)


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MONGODB成功', result)


def next_page(page_number):
    print('正在翻页', page_number)
    browser.find_element_by_id('pnnext').click()
    get_info()
    time.sleep(2)


def main():
    search()
    for i in range(2, 100):
        next_page(i)
    browser.close()


if __name__ == '__main__':
    main()
