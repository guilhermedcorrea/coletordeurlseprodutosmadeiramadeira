from itertools import zip_longest
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


class Madeira:
    driver = webdriver.Chrome(ChromeDriverManager().install())

    def __init__(self):
        self.urls_produto = []
        self.dict_produtos = {}
        self.items = []
    
    def scroll(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    def get_urls(self):
        lista_dicts = []
        data = pd.read_excel("urlmadeira.xlsx")
        for i, row in data.iterrows():
            self.driver.get(row[0])
            time.sleep(1)

            dict_produtos = {}
            self.scroll()
            
            dict_produtos['PaginaProduto'] = row[0]
            dict_produtos['Loja'] = 'MadeiraMadeira'
            dict_produtos['Marca'] = 'Tarkett'
            dict_produtos['EAN'] = 'naoinformado'

            try:
                nome_produto = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/h1')[0].text
                dict_produtos['NomeProduto'] = nome_produto
            
            except:
                print("Nome nao encontrado")

            try:
                categorias = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div/a')
                categoriasurl = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div/a')
                cont = 0
                for categoria in categorias:
                    dict_produtos[categoria.text] = categoriasurl[cont].get_attribute('href')
                    cont+=1
                    
            except:
                print("error categoria")
            
            try:
                seller_vendendo = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/p/a')[0].text
                dict_produtos['SellerVendendo'] = seller_vendendo
            except:
                print("erro Seller")
            
            try:
                preco = self.driver.find_elements_by_xpath(
                    '//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/span')[0].text
                dict_produtos['PRECO'] = preco
            except:
                print("Error")

            try:
                opcoes_cores = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div/span')
                cont = 0
                for opcoes in opcoes_cores:
                    dict_produtos["cores"+str(cont)] = opcoes.text
                    cont+=1
            except:
                print("erro cores")

            try:
                metro = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[6]/div/div/div/div[1]/input')[0]
                metro = metro.get_attribute('value')
                dict_produtos['MetroProduto'] = metro
            except:
                print("error metro")

            try:
                observacoes = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[1]/div[2]/div/div/p[1]')
                for obs in observacoes:
                    dict_produtos['Observacoes'] = obs.text
            except:
                print("error")

            try:
                imagens = self.driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/ul/li/a/div/img')
                imagcont = 0
                for imagem in imagens:
                    dict_produtos['IMAGEM'+str(imagcont)] = imagem.get_attribute("src").replace("width=256","width=600")
                    imagcont+=1
            except:
                print("error imagem")

            try:
                descricao = self.driver.find_elements_by_xpath('//*[@id="radix-id-0-158-content-product_information"]/div/div/div[1]/div[3]/div')
                for descri in descricao:
                    dict_produtos['DescricaoProduto'] = descri.text
            except:
                print('error')

            lista_referencia = []
            lista_valor = []
            referencia_atributo = self.driver.find_elements_by_xpath(
                    '//*[@id="radix-id-0-158-content-product_information"]/div/div/div/div/div/table/tbody/tr/td[1]')
            for valor in referencia_atributo:
                lista_referencia.append(valor.get_attribute('textContent'))

            valor_atributo = self.driver.find_elements_by_xpath(
                    '//*[@id="radix-id-0-158-content-product_information"]/div/div/div/div/div/table/tbody/tr/td[2]')

            for valor in valor_atributo:
                lista_valor.append(valor.get_attribute('textContent'))

            for keys, values in zip_longest(lista_referencia, lista_valor):
                dict_produtos[keys] = values

            print(dict_produtos)
            lista_dicts.append(dict_produtos)

        datamadeira = pd.DataFrame(lista_dicts)
        datamadeira.to_excel("infosmadeira.xlsx")
   
        


madeira = Madeira()
madeira.get_urls()