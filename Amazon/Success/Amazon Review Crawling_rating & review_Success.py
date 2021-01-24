#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[2]:


asinNum="B08628SJ46"


# In[3]:


base_url="https://www.amazon.com/dp/"


# In[4]:


url=base_url+asinNum


# In[5]:


header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}


# In[6]:


search_response=requests.get(url,headers=header)


# In[7]:


search_response.status_code


# In[8]:


search_response.text


# In[9]:


search_response.cookies


# In[10]:


cookie={} # insert request cookies within{}
def getAmazonSearch(asinNum):
    url="https://www.amazon.com/dp/"+asinNum
    print(url)
    page=requests.get(url,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# In[11]:


def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# In[12]:


def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# In[13]:


product_names=[]
response=getAmazonSearch(asinNum)
soup=BeautifulSoup(response.content, "html.parser")
for i in soup.findAll("span",{'class':'a-size-large product-title-word-break'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list


# In[14]:


product_names


# In[15]:


len(product_names)


# In[16]:


link=[]
for i in range(len(product_names)):
    response=getAmazonSearch(asinNum)
    soup=BeautifulSoup(response.content, "html.parser")
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])


# In[17]:


len(link)


# In[18]:


link


# In[19]:


dates=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-date"}):
            dates.append(i.text)  


# In[20]:


len(dates)


# In[21]:


titles=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-title"}):
            titles.append(i.text)        


# In[22]:


len(titles)


# In[39]:


ratings=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll('i',class_='review-rating'):
            ratings.append(i.get_text())     


# In[42]:


len(ratings)


# In[43]:


reviews=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)


# In[50]:


len(reviews)


# In[51]:


rev={
    'Date':dates,
    'Title':titles,
     'Rating':ratings,
     'Review':reviews,    
    }


# In[52]:


review_data=pd.DataFrame.from_dict(rev, orient='index')
review_data=review_data.transpose()
# pd.set_option('max_colwidth',800)


# In[53]:


review_data.head(5)


# In[54]:


review_data.shape


# In[55]:


review_data.to_csv('Scraping reviews_rating & review2.csv') #converting the dataframe to a csv file so as to use it later for further analysis

# ###word cloud 작업###
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt #to display our wordcloud
# from PIL import Image #to load our image
# import numpy as np #to get the color of our image
#
# #Content-related
# text = open('f.txt', 'r').read()
# stopwords = set(STOPWORDS)
#
# #Appearance-related
# custom_mask = np.array(Image.open('cloud.png'))
# wc = WordCloud(background_color = 'white',
#                stopwords = stopwords,
#                mask = custom_mask,
#                contour_width = 3,
#                contour_color = 'black')
#
# wc.generate(text)
# image_colors = ImageColorGenerator(custom_mask)
# wc.recolor(color_func = image_colors)
#
# #Plotting
# ##plt.imshow(wc, interpolation = 'bilinear')
# ##plt.axis('off')
# ##plt.show()
#
# wc.to_file('Batman_wordcloud.png')