## import modules
import pandas as pd
import requests
from bs4 import BeautifulSoup

## entering specific ASIN for result
asinNum="B08628SJ46"
base_url="https://www.amazon.com/dp/"
url=base_url+asinNum

## sending header
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}
search_response=requests.get(url,headers=header)
search_response.status_code
search_response.text
search_response.cookies

## function to get the content of the page of required query
cookie={} # insert request cookies within{}
def getAmazonSearch(asinNum):
    url="https://www.amazon.com/dp/"+asinNum
    print(url)
    page=requests.get(url,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


## function to get the contents of individual product pages using 'data-asin' number (unique identification number)
def Searchasin(asinNum):
    url="https://www.amazon.com/dp/"+asinNum
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"

## function to pass on the link of 'see all reviews' and extract the content
def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"

## First page product reviews extraction
product_names=[]
response=getAmazonSearch(asinNum)
soup=BeautifulSoup(response.content, "html.parser")
for i in soup.findAll("span",{'class':'a-size-large product-title-word-break'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list

product_names
len(product_names)

## By passing the data-asin numbers, we can extract the 'see all reviews' link for each product in the page
## link ##
## total_reviewws ##
link=[]
total_reviews=[]
for i in range(len(product_names)):
    response=getAmazonSearch(asinNum)
    soup=BeautifulSoup(response.content, "html.parser")
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])
        for i in soup.findAll("div",{'data-hook':"total-review-count"}):
            total_reviews.append(i.text)

link
len(link)
total_reviews
len(total_reviews)

## Now we have the 'see all review' links. Using this link along with a page number, we can extract the reviews in any number of pages for all the products
## dates ##
dates=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-date"}):
            dates.append(i.text)  

dates
len(dates)

## titles ##
titles=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-title"}):
            titles.append(i.text)        

titles
len(titles)

## ratings ##
ratings=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll('i',class_='review-rating'):
            ratings.append(i.get_text())     

ratings
len(ratings)

## reviews ##
reviews=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content, "html.parser")
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)

reviews
len(reviews)

## save data into excel file
# making a data frame with a dictionary form
rev={
    'Date':dates,
    'Title':titles,
     'Rating':ratings,
     'Review':reviews,    
    }

# matching the count of columns and rows
review_data=pd.DataFrame.from_dict(rev, orient='index')
review_data=review_data.transpose()

review_data.head(5)

review_data.shape

# converting the dataframe to a csv file so as to use it later for further analysis
review_data.to_csv('Scraping reviews_rating & review2.csv')