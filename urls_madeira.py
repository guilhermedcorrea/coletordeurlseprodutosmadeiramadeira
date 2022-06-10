import lxml.html as parser
import requests
import csv
import time
import re
import json
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class UrlMadeira:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    def __init__(self):
        self.urls = []
        self.desc_url = {}
        self.paginas = []
        self.categorias = []

    def scroll(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    def get_paginas(self):
        self.driver.get("https://www.madeiramadeira.com.br/busca?q=tarkett&page=1&f=eyJxdWVyeVN0cmluZyI6W119")
        self.scroll()
        time.sleep(1)
        urls_categorias = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[4]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/ul/li/a')
        for urls in urls_categorias:
            url = urls.get_attribute('href')
            self.paginas.append(url)


    def get_urls(self):
        for i in range(1,5):
            url = 'https://www.madeiramadeira.com.br/busca?q=durafloor&page=' + str(i) +'&f=eyJxdWVyeVN0cmluZyI6W119'
            self.driver.get(url)
            self.scroll()
            urls_produto = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[4]/div/div/div/div[2]/div/div[1]/div/div/article/a')
            for produtos in urls_produto:
                produtos = produtos.get_attribute('href')
                print(produtos)
                self.urls.append(produtos)
        '''
        for pagina in self.paginas:
            self.driver.get(pagina)
            time.sleep(1)
            self.scroll()

            urls_produto = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[4]/div/div/div/div[2]/div/div[1]/div/div/article/a')
            for produtos in urls_produto:
                produtos = produtos.get_attribute('href')
                self.urls.append(produtos)
        '''
    def create_excel(self):
        dataurl = pd.DataFrame({'URLS':self.urls})
        dataurl.to_excel("urlmadeiradurafloor.xlsx")

  

urls = UrlMadeira()
urls.get_paginas()
urls.get_urls()
urls.create_excel()
