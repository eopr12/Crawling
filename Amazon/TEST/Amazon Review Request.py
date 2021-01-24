#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver


# In[2]:


# 크롬 드라이버 경로 지정
driver = webdriver.Chrome('C:\Users\Becky\Desktop\backup_becky\파이썬\파이썬 프로그램 다운로드\chromedriver_win32/chromedriver.exe')

# Session & header 설정
session = requests.Session()
session.headers = {"User-Agent": "Chrome/87.0 (Macintosh; Intel Win 10 10_9_5)         WindowsWebKit 3.80.36 (KHTML, like Gecko) Chrome",
                   "Accept": "text/html,application/xhtml+xml,application/xml;\
         q=0.9,imgwebp,*/*;q=0.8"}


# In[3]:


#opening url
driver.execute_script("window.open('https://sellercentral.amazon.com/orders-v3/fba/all?page=1&date-range=last-14');")


# In[ ]:


#finding elements
element = webDriver.findElement(By.xpath("//div[@class="cell-body-title"]/tbody/tr[2]/td[3]/div/div[1]/a']")).click()
#driver.find_element_by_id()
#driver.find_element_by_class_name()
#driver.find_element_by_name()
#webDriver.findElement(By.xpath("//a[@href='']")).click();

#clicking elements
element.click();


# In[ ]:




