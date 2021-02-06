#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[2]:


search_query="cleanser"


# In[3]:


base_url="https://www.amazon.com/s?k="


# In[4]:


url=base_url+search_query


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
def getAmazonSearch(search_query):
    url="https://www.amazon.com/s?k="+search_query
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
response=getAmazonSearch('cleanser')
soup=BeautifulSoup(response.content, "html.parser")
for i in soup.findAll("span",{'class':'a-size-base-plus a-color-base a-text-normal'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list


# In[14]:


product_names


# In[15]:


len(product_names)


# In[16]:


# total_reviews=[]
# response=getAmazonSearch('cleanser')
# soup=BeautifulSoup(response.content, "html.parser")
# for i in soup.findAll("span",{''}): # the tag which is common for all the names of products
#     total_reviews.append(i.text) #adding the product names to the list


# In[17]:


# total_reviews


# In[18]:


# len(total_reviews)


# In[19]:


price=[]
response=getAmazonSearch('cleanser')
soup=BeautifulSoup(response.content, "html.parser")
for i in soup.findAll("span",{'class':'a-price'}): # the tag which is common for all the names of products
    price.append(i.text) #adding the product names to the list


# In[20]:


price


# In[21]:


len(price)


# In[22]:


data_asin=[]
response=getAmazonSearch("cleaser")
soup=BeautifulSoup(response.content, "html.parser")
for i in soup.findAll("div",{'class':"sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"}):
    data_asin.append(i['data-asin'])


# In[23]:


response.status_code


# In[24]:


data_asin


# In[25]:


len(data_asin)


# In[48]:


link=[]
total_reviews=[]
for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content, "html.parser")
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])
        for i in soup.findAll("div",{'data-hook':"total-review-count"}):
            total_reviews.append(i.text)


# In[49]:


len(link)


# In[50]:


link


# In[51]:


total_reviews


# In[52]:


reviews=[]
for j in range(len(link)):
    for k in range(2):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)


# In[53]:


len(reviews)


# In[54]:


rev={
    'URL': link,
    'ASIN': data_asin,
    'product names': product_names,
    'total reviews': total_reviews,
    'price': price,
    'reviews':reviews}


# In[55]:


review_data=pd.DataFrame.from_dict(rev, orient='index')
review_data=review_data.transpose()


# In[56]:


review_data.head(5)


# In[57]:


review_data.shape


# In[58]:


review_data.to_csv('Scraping reviews5.csv') #converting the dataframe to a csv file so as to use it later for further analysis

