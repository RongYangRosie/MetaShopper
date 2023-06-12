import requests
import json
import re
import os
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

from requests.exceptions import RequestException

class AmazonCrawler:
   

    def __init__(self):
        #self.base_url = 'https://www.amazon.com/s'
        self.config = json.load(open('crawler/configuration.json'))
        self.header =  {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                        "Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36 ",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,"
                    "*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1",
        }
        
        self.amazon_store = None
        for store in self.config['stores']:
            if store['name'] == 'Amazon':
                self.amazon_store = store
                break
        
        if self.amazon_store is None:
            raise ValueError('Amazon store not found in configuration file')
        
    

    def query(self, product):
        
        '''query_string = {
            '_nkw': '{}'.format(product)
        }'''
        product_list = list()
        
        url = self.amazon_store['url']
        query_params = self.amazon_store['query_params']
        query_params['k'] = product

     
        
        response = requests.get(url, headers=self.header, params=query_params)
        html = response.text
        

        products = self.parse(html, self.amazon_store)
        product_list.extend(products)

        return product_list
   

 
    def parse(self, html,store):
        soup = BeautifulSoup(html, 'html.parser')
        product_list = list()

        for div in soup.select(store['product_selector']):
           
            try:
                product_tag = div.select_one(store['link_selector'])['href']
                #product_tag = div.find('a', class_='a-link-normal s-no-outline')['href']
                product_link = urljoin(store['url'], product_tag)

                #print(" product_link:", product_link)
                if product_link is None:
                    continue
                product_imgSrc = div.find('img', class_ = 's-image')['src']
                #print("product_img:", product_imgSrc)

                #product_name = div.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()
                product_name = div.select_one(store['name_selector']).get_text()
                #print("product_name:",product_name)
                #product_name = product_aTag.find('.').get_text()
                
                rating_span = div.find("span", {"aria-label": True})
                product_rating   = rating_span.get("aria-label")
                #product_rating = div.find( class_ = 'a-row a-size-small').get('aria-label')
                #print("product_rating:",product_rating)

                product_price_str = div.select_one(store['price_selector']).text.strip()
                #product_price_str = div.find('span', class_ ='a-offscreen').string
                product_price = float(product_price_str[1:].replace(',', ''))
                #print("produce_price:",product_price)
                
                product_source = 'Amazon'
                product_list.append(( product_imgSrc, product_name,  product_link, product_rating, product_price, product_source))
            except:
                continue
        return product_list