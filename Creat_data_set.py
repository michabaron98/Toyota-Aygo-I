#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[2]:


URL='https://www.otomoto.pl/osobowe/toyota/aygo/?search%5Bfilter_enum_generation%5D%5B0%5D=gen-i-2005-2014&search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Bfilter_enum_gearbox%5D%5B0%5D=manual&search%5Bfilter_enum_gearbox%5D%5B1%5D=manual-sequential&search%5Bfilter_enum_damaged%5D=0&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=1&page='


# In[3]:


def get_quantity_of_pages(URL):
    web=requests.get(URL+'1')
    soup=BeautifulSoup(web.text, 'html.parser')
    pages=soup.find_all('span', attrs={'class':'page'})
    last_page=[]
    last_page=str(pages).split('<span class="page">')
    last_page=last_page[-1].split('<')
    #print(last_page)
    end=int(last_page[0])
    
    return end


# In[4]:


end=get_quantity_of_pages(URL)
#end


# In[5]:


def convert_location_into_number(loc):
    switcher = {
        'Dolnośląskie':1,
        'Kujawsko-pomorskie':2,
        'Lubelskie':3,
        'Lubuskie':4,
        'Łódzkie':5,
        'Małopolskie':6,
        'Mazowieckie':7,
        'Opolskie':8,
        'Podkarpackie':9,
        'Podlaskie':10,
        'Pomorskie':11,
        'Śląskie':12,
        'Świętokrzyskie':13,
        'Warmińsko-mazurskie':14,
        'Wielkopolskie':15,
        'Zachodniopomorskie':16
    }      
    return switcher.get(loc, "Voivodeship")


# In[ ]:





# In[6]:


cars=pd.DataFrame(columns=["year","mileage","price","location"])
for i in range(1,end+1):
    New_URL=URL+str(i)
    web=requests.get(New_URL)
    soup=BeautifulSoup(web.text, 'html.parser')
    results=soup.find_all('div', attrs={'class':'offer-item__wrapper'})
    len(results)
    cars_buffor=[]
    cars_buffor1=pd.DataFrame(columns=["year","mileage","price"])
    for result in results:
        list_of_lines=[]
        list_of_lines=str(result).split('\n')
        year=list_of_lines[list_of_lines.index('<li class="ds-param" data-code="year">')+1]
        year=re.findall(r'\d+', year)
        year=int(year[0])
        mileage=list_of_lines[list_of_lines.index('<li class="ds-param" data-code="mileage">')+1]
        mileage=re.findall(r'\d+', mileage)
        mileage="".join(mileage)
        mileage=int(mileage)
        price=list_of_lines[list_of_lines.index('<span class="offer-price__number ds-price-number">')+1]
        price=re.findall(r'\d+', price)
        price="".join(price)
        price=int(price)
        location=list_of_lines[list_of_lines.index('<span class="icon-location-2 ds-location-icon"></span>')+2]
        location=location.split('(')
        location=location[1].split(')')
        location=convert_location_into_number(location[0])
        cars_buffor.append([year,mileage,price,location])
    cars_buffor1=pd.DataFrame(cars_buffor, columns=["year","mileage","price","location"])
    #print(cars_buffor1)
    #cars_buffor1=
    cars=cars.append(cars_buffor1, ignore_index = True)


# In[7]:


cars


# In[8]:


cars.to_csv("Toyota_aygo_I.csv", index=False)


# In[ ]:




