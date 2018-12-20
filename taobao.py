from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import time
import pymongo

from config import *

browser = webdriver.Chrome()
whait = WebDriverWait(browser,20)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def search():
    try:
        browser.get("https://www.taobao.com/")

        input = WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"#q"))
        )
        submit = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-search"))
        )
        input.send_keys("戒指女 纯银")
        submit.click()
        # login_in()
        total = whait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.total")))
        num = re.compile('(\d+)').search(total.text).group(1)
        get_products()
        return num
    except TimeoutException:
        return search()

def next_page(page_num):

    try:
        input = whait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.input:nth-child(2)"))
        )
        # submit = whait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn"))
        # )
        # submit = browser.find_elements_by_css_selector('.btn J_Submit')
        submit = whait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#spulist-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        # time.sleep(2)
        # browser.execute_script("arguments[0].click();", element)
        input.clear()
        input.send_keys(page_num)
        submit.click()
        whait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'li.active > span:nth-child(1)'),str(page_num))
        )
        get_products()
    except TimeoutException:
        return next_page(page_num)
def handle_screen_size(item):
    try:
        return item.select('.important-key')[0].get_text()
    except Exception:
        return None

def handle_image(item):
    try:
        return item.select(".img")[0]["src"]
    except Exception:
        return None

def handle_price(item):
    try:
        return item.select(".price")[0].get_text()
    except Exception:
        return item.select(".col")[0].get_text()

def handle_customer_number(item):
    try:
        return item.select(" .week-sale")[0].get_text()
    except Exception:
        return None

def get_products():
    browser.execute_script("""var h = document.body.scrollHeight-1500,
        k = 0;
    var timer = setInterval(function() {
        k += 150;
        console.log(k);
        if (k > h) clearInterval(timer);
        window.scrollTo(0,k);
    }, 500);""")
    whait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#J_SPUBlankRow11 > div:nth-child(4) > div > div.img-box'))
    )
    whait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#spulist-grid .m-grid .grid-container.row .blank-row .grid-item'))
    )
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html,"html.parser")
    doc = pq(html)
    # items1 = doc('#spulist-grid .m-grid .grid-container.row .blank-row .grid-item').items()
    items1 = soup.select('#spulist-grid .m-grid .grid-container.row  .grid-item')
    # items2 = doc("#spulist-grid .m-grid .grid-container.row .blank-row.col .grid-item.col").items()
    for item in items1:
        # print(item.select(".img"))
        product={

            "screen_size": handle_screen_size(item),
            "image" : handle_image(item),
            "tittle" : item.select(".product-title")[0]["title"],
            "price" : handle_price(item),

            "customer-number" : handle_customer_number(item),
            "talk-number" : item.select(".comment-row")[0].get_text()


        }
        print(product)
        time.sleep(5)
        save_mongo(product)


def save_mongo(result):
    try:
        if db[MONGO_TABLE].insert_one(result):
            print("success")
    except Exception as e:
        print ("fail")

def login_in():
    username = whait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"#TPL_username_1"))
    )

    pwd = whait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#TPL_password_1"))
    )
    sumbit =whait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_SubmitStatic"))
    )

    username.send_keys()
    pwd.send_keys()
    sumbit.click()

if __name__=="__main__":
    s = search()
    print(s)
    for i in range(2,int(s)+1):
        print(i)
        next_page(i)




