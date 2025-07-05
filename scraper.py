import pandas as pd 
from bs4 import BeautifulSoup 
import requests 

def scan_url(url): # Return the full html !
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.9",
      "Connection": "keep-alive",
      "DNT": "1",
      "Upgrade-Insecure-Requests": "1",
  }
  response = requests.get(url , headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  return soup 

def get_href(url) : # Return every HREF from an url !
  all_links = []
  soup = scan_url(url)
  divs = soup.find_all('div' , attrs = {'class' : 'x-card x-card-flex'})
  for i in range(len(divs)) : 
    a = divs[i].find('a' , {'class' : 'ux-action'})
    link = a.get('href')
    all_links.append(link)
  return all_links

def get_data(url) :
  titles = []
  prices = []
  rates = []
  reviews = []
  links_to_get = get_href(url)
  df = pd.DataFrame({'Title' : titles , 'Price' : prices , 'Reviews' : reviews, 'Rates' : rates}) # to ignore local variable problem !
  for i in links_to_get :
    soup = scan_url(i)
    if soup is None:
        titles.append(None)
        prices.append(None)
        rates.append(None)
        continue

    title_div = soup.find('div', attrs = {'class' : 'vim x-item-title'})
    title = None
    if title_div:
      title_span = title_div.find('span' , attrs = {'class' : 'ux-textspans'})
      if title_span:
        title = title_span.text.strip()

    price_div = soup.find('div', attrs = {'class' : 'x-price-primary'})
    price = None
    if price_div:
      price_span = price_div.find('span' , attrs = {'class' : 'ux-textspans'})
      if price_span:
        price = price_span.text.strip()

    rate_div = soup.find('div' , attrs = {'class' : 'vim x-star-rating'})
    rate = None
    if rate_div:
      rate_span = rate_div.find('span' , attrs = {'class' , 'ux-textspans'})
      review_span = rate_div.find('span' , attrs = {'class' , 'ux-textspans ux-textspans--PSEUDOLINK'})
      if rate_span and review_span :
        rate = rate_span.text
        review = review_span.text

    titles.append(title)
    prices.append(price)
    rates.append(rate)
    reviews.append(review)
    df = pd.DataFrame({'Title' : titles , 'Price' : prices , 'Reviews' : reviews, 'Rates' : rates})
  return df


# In my example i will use this url : url = 'https://www.ebay.com/t/Computers-Tablets-Network-Hardware/58058/bn_1865247'
# my usage : ebay_products = get_data(url) 


def clean_data(df) : 
  df.dropna(subset=['Title','Price'], inplace = True)
  df.Price = df.Price.str.replace('$','')
  df.Price = df.Price.str.replace('C','')
  df.Reviews = df.Reviews.str.split(' ').str[0]
  return df 

df.to_csv('output.csv', index = False)
