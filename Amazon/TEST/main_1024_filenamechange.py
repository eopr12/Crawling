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
now = datetime.datetime.now()  # 현재 시간 출력
start_time = now.strftime('%Y-%m-%d %H:%M:%S')  # 형식 문자열 반환

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
# noinspection PyUnusedLocal
def main(URL):
    url_list = []
    image_list = []
    #brand_list = []
    title_list = []
    rating_list = []
    originalprice_list = []
    pricereduction_list = []

    # zip code 변경하기
    # We ship internationally 팝업창 클릭
    #driver.find_elements_by_tag_name("input", "SELECT_LOCATION")
    # zip code 클릭
    # driver.find_element_by_id("nav-global-location-slot").click()
    # 미국 zip code 입력
    #driver.find_element_by_id("GLUXZipUpdateInput").send_keys('10001')
    # apply 클릭
    #driver.find_element_by_class_name("input").click()

    next_link = URL.format(keyword)

    while (next_link):
        driver.get(next_link)
        source = driver.page_source
        # _url, _img, _brd, _ttl, _rat, _orp, _prd, next_link = components(source)
        _url, _img, _ttl, _rat, _orp, _prd, next_link = components(source)
        if next_link != 0:
            next_link = URL_SEL + str(next_link)
            url_list += _url
            image_list += _img
            #brand_list += _brd
            title_list += _ttl
            rating_list += _rat
            originalprice_list += _orp
            pricereduction_list += _prd
            time.sleep(randint(1, 5))
            #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list
            return url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list

# Beautiful Soup
#####url / image / brand / title / rating / original price / price reduction 수집 + next link#####
# noinspection PyUnreachableCode
def components(source):
    print("components 크롤링 시작")

    url_list = []
    image_list = []
    #brand_list = []
    title_list = []
    rating_list = []
    originalprice_list = []
    pricereduction_list = []

    soup = bs(source, 'html.parser')

    #url (링크 필요)
    print("===========================")
    print("====== url 찾기 시작 =======")
    u_list = soup.find_all(
        'div', class_="a-section a-spacing-none a-spacing-top-small")
    for url in u_list:
        urll = url.find_all('a', class_='a-link-normal a-text-normal')
        for u in urll:
            url_list.append(u.attrs['href'])
    print("=========================")
    print("====== url 찾기 끝 =======")
    print("=========================")
#    return(1)

    #image (이미지 필요)

    # For Texts with img tag
    print("===========================")
    print("===== image 찾기 시작 ======")
    htmlText = """<img src = "https://m.m.media-amazon.com/images/I/51fAh2a03cL._AC_UL320_.jpg">"""
    soup = bs(htmlText)
    images = soup.find_all("img")
    for i in images:
        image_list.append("src")

    #i_list = soup.find_all(
    #     'div', class_= "a-section aok-relative s-image-square-aspect")
    #for img in i_list:
    #     image = img.find_all("img")
    #     for i in image:
    #         image_list.append(i.get["src"])

    print("=========================")
    print("===== image 찾기 끝 ======")
    print("=========================")
    # return(1)
    #
    # brand(zip코드 미국 필수)
    #print("===========================")
    #print("===== brand 찾기 시작 ======")
    #b_list = soup.find_all(
    #    #'div', class_ = "a-row a-size-base-plus a-color-base") 오토광고 html
    #    'div', class_="a-row a-size-base a-color-secondary")
    #for brd in b_list:
    #    brand_list.append(brd.get_text())
    #print("=========================")
    #print("===== brand 찾기 끝 ======")
    #print("=========================")
    # return(1)
    #
    # ASIN
    # print("==========================")
    # print("===== ASIN 찾기 시작 ======")
    # a_list = soup.find_all(
    #     'div', data-asin_="")
    # print("========================")
    # print("===== ASIN 찾기 끝 ======")
    # print("========================")
    # return(1)
    #
    # # title (링크 필요)
    print("===========================")
    print("===== title 찾기 시작 ======")
    t_list = soup.find_all('span', class_="a-size-base-plus a-color-base a-text-normal")
    for ttl in t_list:
        title_list.append(ttl.get_text())
    print("===========================")
    print("====== title 찾기 끝 =======")
    print("===========================")
#    return (1)

    #rating (링크 필요)
    print("===========================")
    print("===== rating 찾기 시작 ======")
    r_list = soup.find_all(
        'span', class_="a-icon-alt")
    for rat in r_list:
        rating_list.append(rat.get_text())
    print("===========================")
    print("====== rating 찾기 끝 =======")
    print("===========================")
    #    return (1)

    # original price
    print("===================================")
    print("===== original pice 찾기 시작 ======")
    #op_list = soup.find_all(
    #    'a', class_="a-size-base a-link-normal a-text-normal")
    #for opc in op_list:
    #        originalprice_list.append(opc.get_text())

    #op_list = soup.find_all(
    #    'span', class_="a-offscreen")
    #for opc in op_list:
    #        originalprice_list.append(opc.get_text())

    op_list = soup.find_all('span', class_ = "a-price a-text-price")
    for opc in op_list:
           originalprice_list.append(opc.get_text())

    print("====================================")
    print("====== original price 찾기 끝 =======")
    print("====================================")

    # price reduction
    print("=====================================")
    print("===== price reduction 찾기 시작 ======")
    prd_list = soup.find_all(
         'span', class_="a-offscreen")
    for prd in prd_list:
            pricereduction_list.append(prd.get_text())
    print("=====================================")
    print("====== price reduction 찾기 끝 =======")
    print("=====================================")

    try:
        next_butt = soup.find_all('li', class_='a-last')
        if next_butt == []:  # [] ==>다음 페이지가 아직 더 남았다.
            #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list, 0
            return url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_listt, 0
        next_link = next_butt[0].find_all('a')[0].attrs['href']
#        if url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list == None
#            return " ", 0
    except:
        #0 ==>다음페이지가 있으면(=0이 아니라면) 다시한번 다음 page 가서 url 긁어와라
        #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list, 0
        return url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list, 0
        #print(len(url_list),len(image_list), len(title_list), len(brand_list), len(rating_list), len(originalprice_list), len(pricereduction_list))
    print(len(url_list), len(image_list), len(title_list), len(rating_list), len(originalprice_list), len(pricereduction_list))
    #return url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list, next_link
    return url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list, next_link

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
#url_list, image_list, brand_list, title_list, rating_list, originalprice_list, pricereduction_list = main(URL.format(keyword))
url_list, image_list, title_list, rating_list, originalprice_list, pricereduction_list = main(URL.format(keyword))

# dataframe 생성
a = {"url": url_list, "image": image_list, "title": title_list, "rating": rating_list, "original price": originalprice_list, "price reduction": pricereduction_list}

df = pd.DataFrame.from_dict(a, orient = 'index')
df.transpose()
#df = pd.DataFrame(
#    {
#        #"brnad" : brand_list,
#        # "ASIN" : asin_list,
#        "url" : url_list,
#        #"image" : image_list,
#        "title": title_list,
#        "rating" : rating_list,
#        "originalprice" : originalprice_list,
#        #"pricereduction" : pricereduction_list
#    }
#)
# Excelwriter 생성
writer = pd.ExcelWriter('test1.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer)
writer.save()
print("===============종료==============")
print("components 크롤링 완료")

########################################################
####################문제점,Q&A###########################
########################################################
#1. brnad 태그는 zip code를 설정해야 나타나는 부분이라 zip code 클릭 및 입력 코드 추가 필요
#ㄴ zip code 코드는 def 안에 넣어줘야하는건가?
#2. 파일명을 바꿨음에도 불구하고 계속해서 components_test4 이름으로 저장됨
#3. original price태그와 pricereduction태그를 각각 입력하면 original price만 추출됨
#4. 엑셀데이터 결과물 보면 sponsored ad 2번째~4번째 상품이 빠져있음
#5. pandas에서 Nonetype Error가 일어날 경우 Try except 코드를 main 코드 안에 넣어주는게 맞나요?