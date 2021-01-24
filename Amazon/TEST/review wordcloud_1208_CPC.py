###Review 크롤링 작업###
import selenium
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

URL_SEL = "https://www.amazon.com/SK-hynix-Gold-NAND-Internal/product-reviews/B07SNHB4RC/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

# 크롬 드라이버 경로 지정
driver = webdriver.Chrome('C:/Users/Becky/chromedriver_win32/chromedriver.exe')

# Session & header 설정
session = requests.Session()
session.headers = {"User-Agent": "Chrome/68.0 (Macintosh; Intel Win 10 10_9_5)\
         WindowsWebKit 3.80.36 (KHTML, like Gecko) Chrome",
                   "Accept": "text/html,application/xhtml+xml,application/xml;\
         q=0.9,imgwebp,*/*;q=0.8"}

# def main(URL):
#     review_list = []
#
#     next_link = URL.format(keyword)
#     while (next_link):
#         driver.get(next_link)
#         source = driver.page_source
#         _review = review(source)
#         if next_link != 0:
#             next_link = URL_SEL + str(next_link)
#             review_list += _review
#             time.sleep(randint(1, 5))
#             return review_list
#
# def review(source):
#     print("review 크롤링 시작")
#
#     review_list = []
#
#     soup = bs(source, 'html.parser')
#
#     print("=============================")
#     print("====== review 수집 시작 =======")
#     review_list = soup.find_all(
#         'div', class_="a-section a-spacing-none a-spacing-top-small")
#     for review in review_list:
#         revieww = review.find_all('a', class_='a-link-normal a-text-normal')
#     print("============================")
#     print("====== review 수집 끝 =======")
#     print("============================")
#
#     try:
#         next_butt = soup.find_all('li', class_='a-last')
#         if next_butt == []:
#             return url_list, 0
#         next_link = next_butt[0].find_all('a')[0].attrs['href']
#
#     except:
#         return review_list, 0
#     print(len(review_list))
#     return review_list, next_link

def review(review_set):
    global URL_SEL, driver  # 셀레니움 드라이버
    rating_data = []
    review_data = []  # 리스트 처리

    # enumerate() ==> for in과 다르게 몇 번째 반복문인지 옆에 나타내고 싶을 때 사용
    for aa, review in enumerate(review_set):  # Q aa 뭐임?

        rq = requests.get(URL_SEL + review)  # url속 html 가져오기
        soup = bs(rq.text, 'html.parser')  # html 가져와서 parsing
        for revieww in soup.find('div', {'class':'a-section celwidget'}).find('div', {'a-row a-spacing-small review-data'}): # 원하는 값 찾기(클래스로 찾기)
            revieww == review_html

        review = ""
        if review_html[0].get_text():
            review += review_html[0].get_text().strip()

        else:
            for rev in review_html:
                tt_rev = rev.find_all('p')  # p라는 글자를 포함하는 태그를 가져옴
                for tt in tt_rev:
                    review += tt.get_text()
        review_data.append(review)  # article list에 추가

        rating = ""
        try:
            rating_html = soup.find_all('i').text
            for rat in rating_html:
                rating += rat.get_text().strip()
                rating += "\n"
            rating_html.append(rating)
        except:
            rating_html.append(rating)
    return review_data, rating_data

# 크롤링 결과물 txt 파일로 저장하기
f = open ('C:/Users/Becky/anaconda3/envs/PycharmProjects/pycharm files/crawling/amazon/wordcloud/Batman_wordcloud-master', 'w', encoding = 'utf-8')

for r in review:
    data = r.SaveFormat()

    f.write(data)
    f.write('\n')

f.close()

###word cloud 작업###
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt #to display our wordcloud
from PIL import Image #to load our image
import numpy as np #to get the color of our image

#Content-related
text = open('f.txt', 'r').read()
stopwords = set(STOPWORDS)

#Appearance-related
custom_mask = np.array(Image.open('cloud.png'))
wc = WordCloud(background_color = 'white',
               stopwords = stopwords,
               mask = custom_mask,
               contour_width = 3,
               contour_color = 'black')

wc.generate(text)
image_colors = ImageColorGenerator(custom_mask)
wc.recolor(color_func = image_colors)

#Plotting
##plt.imshow(wc, interpolation = 'bilinear')
##plt.axis('off')
##plt.show()

wc.to_file('Batman_wordcloud.png')

