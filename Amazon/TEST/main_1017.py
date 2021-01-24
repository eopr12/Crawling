from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
from random import randint
import openpyxl
import time
import datetime
import re
import random
from collections import Counter
import os
import pandas as pd

# delay 주는법 driver.implicitly_wait(3)
# Setting

# keyword : 띄어쓰기는 +로 연결
keyword = "fake+socks"

###########################################################################
###########################################################################
# 크롤링 시간 측정
now = datetime.datetime.now() #현재 시간 출력
start_time = now.strftime('%Y-%m-%d %H:%M:%S') #형식 문자열 반환

URL = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
URL_SEL = "https://www.amazon.com/"

# 크롬 드라이버 경로 지정
driver = webdriver.Chrome('C:/Users/Becky/chromedriver_win32/chromedriver.exe')

# Session & header 설정
session = requests.Session()
session.headers = {"User-Agent": "Chrome/68.0 (Macintosh; Intel Win 10 10_9_5)\
         WindowsWebKit 3.80.36 (KHTML, like Gecko) Chrome",
                   "Accept": "text/html,application/xhtml+xml,application/xml;\
         q=0.9,imgwebp,*/*;q=0.8"}
###########################################################################
###########################################################################

# Selenium
#####url / image / brand / title / rating / original price / price reduction 수집 + next link#####
def main(URL):
    #url_list = []
    #image_list = []
    #brand_list = []
    title_list = []
    #rating_list = []
    #originalprice_list = []
    #pricereduction_list = []

    next_link = URL.format(keyword)

    while (next_link):
        driver.get(next_link)
        source = driver.page_source
        #_url, _img, _brd, _ttl, _rat, _orp, _prd, next_link = components(source)
        _tmp = components(source)
    try:

        if next_link != 0:
            next_link = URL_SEL + next_link
            #url_list += _url
            #image_list += _img
            #brand_list += _brd
            title_list += _tmp
            #rating_list += _rat
            #originalprice_list += _orp
            #pricereduction_list += _prd
            time.sleep(randint(1, 5))
            #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list
            return title_list
    except:
        #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list
        return title_list
# Beautiful Soup
#####url / image / brand / title / rating / original price / price reduction 수집 + next link#####
def components(source):
    print("components 크롤링 시작")

    # url_list = []
    # image_list = []
    # brand_list = []
    # title_list = []
    # rating_list = []
    # originalprice_list = []
    # pricereduction_list = []
    #
    # soup = bs(source, 'html.parser')
    #
    # # url (링크 필요)
    # u_list = soup.find_all(
    #     'div', class_="a-section a-spacing-none a-spacing-top-small")
    # print("====================")
    # print("===== 찾기 시작 ======")
    # for url in u_list:
    #     urll = url.find_all('a', class_='a-link-normal a-text-normal')
    #     for u in urll:
    #         url_list.append(u.attrs['href'])
    # print("====================")
    # print(url_list)
    # print("====================")
    #
    # return 1 #
    #
    # # image (이미지 필요)
    # i_list = soup.find_all(
    #     'div', class_="a-section a-spacing-none s-image-overlay-black")
    # for img in i_list:
    #     image = img.find_all('div', class_='a-section aok-relative s-image-tall-aspect')
    #     for i in image:
    #         image_list.append(i.attrs['img src'])
    #
    # # brand
    # b_list = soup.find_all(
    #     'div', class_="a-row a-size-base a-color-secondary")
    # for brd in b_list:
    #     brand = brd.find.all('span', class_='a-size-base-plus a-color-base')
    #     for b in brand:
    #     brand_list.append(b.attrs['span'])
    #
    # # ASIN ==> Q div data-asin 이라 'div', data-asin_ = "~~~" 이렇게하면 안되는데 어떤식으로 코드를 입력해야하나욥?ㅇ0ㅇ
    # a_list = soup.find_all(
    #     'div', data-asin_="")
    #
    # # title (링크 필요)
    # t_list = soup.find_all(
    #     'h2', class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")
    # for ttl in t_list:
    #     title = ttl.find_all('a', class_='a-link-normal a-text-normal')
    #     for t in title:
    #         title_list.append(t.attrs['href'])

    print("====TITLE====")
    t_list = soup.find_all('span', class_="a-size-base-plus a-color-base a-text-normal")
    for tmp in t_list:
        title_list.append(tmp.get_text())
    print(title_list)
    return (1)


#     # rating (링크 필요)
#     r_list = soup.find_all(
#         'div', class_="a-section a-spacing-none a-spacing-top-micro")
#     for rat in r_list:
#         rating = rat.find_all('a', class_="a-row a-size-small")
#         for r in rating:
#             rating_list.append(r.attrs['div'])
#
#     # original price
#     op_list = soup.find_all(
#         'div', class_="a-row")
#     for opc in op_list:
#         original = opc.find_all('span', class_="a-price")
#         for o in original:
#             originalprice_list.append(o.attrs['span'])
#
#     # price reduction
#     pr_list = soup.find_all(
#          'div', class_="a-row")
#     for prd in pr_list:
#         reduction = prd.find.all('span', class_="a-price a-text-price")
#         for p in reduction:
#             pricereduction_list.append(p.attrs['span'])
#
#     try:
#         next_butt = soup.find_all('li', class_='a-last')
#         next_link = next_butt[0].find_all('a')[0].attrs['href']
#     except:
#         return url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list, 0 #다음페이지가 있으면(=0이 아니라면) 다시한번 다음 page 가서 url 긁어와라
#
#     print(len(url_list),len(image_list), len(title_list), len(rating_list), len(originalprice_list), len(pricereduction_list))
#
#     return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list, next_link
#
#     #     is_abstract = k.get_text()
#     #     if is_abstract == 'Abstract':
#     #         url_list.append(k.attrs['href'])
#     #     else :
#     #         if not 'ref' in k.attrs['href']:
#     #             if not k.attrs['href'] in url_list:
#     #                 non_abs_url.append(k.attrs['href'])
#     # return url_list, non_abs_url
#
######엑셀 저장#######
# url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list = main(URL.format(keyword))
title_list = main(URL.format(keyword))

# dataframe 생성
df = pd.DataFrame(
    {
        #"brnad" : brand_list,
        #"ASIN" : asin_list,
        #"url" : url_list,
        #"image" : image_list,
        "title" : title_list,
        #"rating" : rating_list,
        #"originalprice" : originalprice_list,
        #"pricereduction" : pricereduction_list
    }
)
# Excelwriter 생성
writer = pd.ExcelWriter('components_test1.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer)
writer.save()
print("===============종료============")
print("components 크롤링 완료")

#################################################
###################Q&A###########################
#################################################