import requests
import json
import re
import os
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

from requests.exceptions import RequestException

class EbayCrawler:
    def __init__(self):
        self.base_url = 'https://www.ebay.com/sch/i.html'
        self.config = json.load(open('crawler/configuration.json'))
        self.header = {
            'user-agent': USER_AGENT,
            'From': 'personal@domain.com'  
        }

        self.ebay_store = None
        for store in self.config['stores']:
            if store['name'] == 'eBay':
                self.ebay_store = store
                break
        
        if self.ebay_store is None:
            raise ValueError('Ebay store not found in configuration file')
        
    def query(self, product):
        
        '''query_string = {
            '_nkw': '{}'.format(product)
        }'''
        product_list = list()
        
        url = self.ebay_store['url']
        query_params = self.ebay_store['query_params']
        query_params['_nkw'] = product

     
       
        response = requests.get(url, headers=self.header, params=query_params)
        html = response.text

        products = self.parse(html, self.ebay_store)
        product_list.extend(products)

        return product_list

    def parse(self, html,store):
        
        soup = BeautifulSoup(html, 'html.parser')
        product_list = list()
        for li in soup.select(store['product_selector']):
            product_img = li.find('img')
            if product_img is not None:
                product_imgSrc = product_img['src']
                #print("product_imgSrc:",product_imgSrc)

            product_aTag = li.select_one(store['link_selector'])
            if product_aTag is not None:
                
                product_link = product_aTag.get('href')
                #print("product_link:",product_link)
                element = li.select_one(store['name_selector'])
                
                if element is not None:
                    product_name = element.text
                else:
                    product_name = None
                #print("product_name:",product_name)
            if product_name is None:
                continue
            price_str = li.select_one(store['price_selector']).string
            if price_str is None:
                continue
            product_price = float(price_str[1:].replace(',', ''))
            #print("product_price:",product_price)

            product_rating = li.find('span', class_='s-item__seller-info-text')
            if product_rating is not None:
                product_rating = product_rating.text.strip() 
                percentage_regex = r'\d+(\.\d+)?%'
                match = re.search(percentage_regex, product_rating)
                if match:
                    product_rating = match.group()
                    product_source  = 'eBay'
                    product_list.append(( product_imgSrc, product_name, product_link,  product_rating, product_price, product_source))
            #print("product_rating:",product_rating)
            
        return product_list


