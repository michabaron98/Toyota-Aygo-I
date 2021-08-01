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


cars=pd.DataFrame(columns=["year","mileage","price"])
for i in range(1,7):
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
        cars_buffor.append([year,mileage,price])
    cars_buffor1=pd.DataFrame(cars_buffor, columns=["year","mileage","price"])
    #print(cars_buffor1)
    cars=cars.append(cars_buffor1, ignore_index = True)


# In[4]:


cars


# In[5]:


cars.to_csv("Toyota_aygo_I.csv", index=False)


# In[ ]:




