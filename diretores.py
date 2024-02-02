from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def ler_pagina():
    a=driver.page_source
    with open('some_file.html', 'w', encoding="utf-8") as f:
        f.write(a)
        
def pegar():
    try: 
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    with open('some_file.html', 'r', encoding="utf-8") as f:
        html = f
        parsed_html = BeautifulSoup(html,features="lxml")
    elements = parsed_html.find_all("span", {"class": "prettify"})
    try:
        return elements[0].text
    except:
        return

def main():
    try:
        df = pd.read_csv("ratings.csv")
    except:
        df = pd.read_csv("ratings.csv", sep = ';')
    urls = df["Letterboxd URI"]
    titulos = df["Name"]
    try:
        f = open("i.txt", "r")
    except:
        f = open("i.txt", "w")
        f.write(str(0))
        f.close()
        f = open("i.txt", "r")
    j = int(f.read())
    for i in range(j,len(urls)):
        f = open("i.txt", "w")
        f.write(str(i))
        f.close()
        try:
            driver.get(urls[i])
        except:
            pass
        time.sleep(1)
        ler_pagina()
        diretor = pegar()
        df.loc[df['Name'] == titulos[i], 'Diretores'] = diretor
        df.to_csv('ratings.csv', index=False)
    f = open("i.txt", "w")
    f.write(str(0))
    f.close()
    df2 = df.pivot_table(index = ['Diretores'], aggfunc ='size')
    f = open("diretores.txt", "w")
    f.write(df2.sort_values(ascending=False).to_markdown())
    f.close()
    print("Fim")
main()