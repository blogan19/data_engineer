import requests
from bs4 import BeautifulSoup
import random


def get_patients(): 
    url = 'https://github.com/emisgroup/exa-data-eng-assessment/tree/main/data'
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    urls = []
    for a in soup.find_all('a',{'class':'js-navigation-open Link--primary'},href=True):
        a = f'https://raw.githubusercontent.com{a["href"].replace("/blob","")}'
        urls.append(a)

    return random.choice(urls)



