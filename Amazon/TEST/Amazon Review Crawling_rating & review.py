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


# In[ ]:


titles=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-title"}):
            titles.append(i.text)        


# In[ ]:


len(titles)


# In[ ]:


ratings=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-star-rating"}):
            ratings.append(i.text)     


# In[ ]:


len(ratings)


# In[ ]:


reviews=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)


# In[ ]:


len(reviews)


# In[ ]:


rev={
    'Date':dates,
    'Title':titles,
     'Rating':ratings,
     'Review':reviews,    
    }


# In[ ]:


review_data=pd.DataFrame.from_dict(rev)
pd.set_option('max_colwidth',800)


# In[ ]:


review_data.head(5)


# In[ ]:


review_data.shape


# In[ ]:


review_data.to_csv('Scraping reviews_rating & review.csv') #converting the dataframe to a csv file so as to use it later for further analysis

