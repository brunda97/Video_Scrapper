
# coding: utf-8

# In[72]:


import sys
#!{sys.executable} -m pip install selenium
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
import webbrowser
import re
import json

URLS=[]
data={}
def URL_List(URL):
    BROWSER = webdriver.Chrome(executable_path='C:/Users/Brunda/Downloads/chromedriver_win32/chromedriver.exe')
    BROWSER.get(URL)
    time.sleep(3)
    HTML = BROWSER.page_source
    SOUP = BeautifulSoup(HTML, "lxml")
    LECTURES= SOUP.findAll('div', attrs={'class' : 'lec_thumb'})   
    for LECTURE in LECTURES:
            for LINK in LECTURE.find_all('a',href=True):   
                URL_LINK="http://videolectures.net"+LINK['href']
                URLS.append(URL_LINK)
                break 
    BROWSER.close()
    BROWSER.quit()
    
def Extract_Data(URL):
    HTML = requests.get(URL, timeout=None)
    SOUP = BeautifulSoup(HTML.text, "lxml")
    TITLE=SOUP.find("span", {"id": "vl_desc"})
    DESC=SOUP.find("div", {"class": "wiki"})
    DESCRIPTION=""
    if DESC:
        DESCRIPTION=DESC.find('p').text
    if TITLE:
        X=TITLE.find('h2').text
        Y=TITLE.text.split('\n')
        AUTHOR=""
        ORGANISATION=""
        PUBLISHED=""
        RECORDED=""
        VIEWS=""
        for ITEM in range(len(Y)):
            if re.match(r"author:+", Y[ITEM].strip()):
                AUTHOR=Y[ITEM].split(':')[1].lstrip()[:-2]
                ORGANISATION=Y[ITEM+1].lstrip()
            elif re.match(r"presenter:+", Y[ITEM].strip()):
                AUTHOR=Y[ITEM].split(':')[1].lstrip()[:-2]
                ORGANISATION=Y[ITEM+1].lstrip()
            elif re.match(r"published:+", Y[ITEM].strip()):
                PUBLISHED=Y[ITEM].split(':')[1].strip()[:-1]
            elif re.match(r"recorded:+", Y[ITEM].strip()):
                RECORDED=Y[ITEM].split(':')[1].strip()[:-1]
            elif re.match(r"views:+", Y[ITEM].strip()):
                VIEWS=Y[ITEM].split(':')[1].strip()
        #print(X)
        #print(URL)
        #print(AUTHOR)
        #print(ORGANISATION)
        #print(PUBLISHED)
        #print(RECORDED)
        #print(DESCRIPTION)
        #print(VIEWS)
        if DESCRIPTION!="":
            data[URL]= {
                        "Title": X,
                        "Author": AUTHOR,
                        "Organisation":ORGANISATION,
                        "Description":DESCRIPTION,
                        "Views":VIEWS,
                        "Published":PUBLISHED,
                        "Recorded":RECORDED                                               
                    }
                    
        else:
                data[URL]= {
                        "Title": X,
                        "Author": AUTHOR,
                        "Organisation":ORGANISATION,
                        "Views":VIEWS,
                        "Published":PUBLISHED,
                        "Recorded":RECORDED                                               
                    }
                    
            
if __name__ == '__main__':
    #Data science keyword to be searched
    URL1 = 'http://videolectures.net/Top/Data_Science/#o=rec&t=vl,vtt'   
    URL2='http://videolectures.net/Top/Data_Science/#o=rec&t=vl,vtt&p=2'
    URL3='http://videolectures.net/Top/Data_Science/#o=rec&t=vl,vtt&p=3'
    URL_List(URL1)
    URL_List(URL2)
    URL_List(URL3)
    for URL in URLS:
        Extract_Data(URL)
    with open('Brunda_BabuPrasad_Task2_data.json', 'w') as fw:
        json.dump(data, fw, sort_keys=True, indent=4)

