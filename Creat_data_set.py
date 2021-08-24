from numpy import zeros
from numpy.lib.utils import info
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_quantity_of_pages(URL):
    """
    Funtcion returns quantity of pages
    
    Variables:
    URL - (string) URL of website Example:"https://www.otomoto.pl/" 
    """
    web=requests.get(URL+'1')
    soup=BeautifulSoup(web.text, 'html.parser')
    pages=soup.find_all('span', attrs={'class':'page'})
    last_page=[]
    last_page=str(pages).split('<span class="page">')
    last_page=last_page[-1].split('<')
    #print(last_page)
    end=int(last_page[0])
    #print(end)
    return end
def convert_location_into_number(loc):
    """
    Funtcion converts name of polish voidvoidship into number
    
    Variables:
    loc - name of voidvoidship: 
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
    """
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
    return switcher.get(loc)
def get_details_from_offer_item_wraper(URL):
    end=get_quantity_of_pages(URL)

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
    return cars
def get_links_to_offers(URL):
    end=get_quantity_of_pages(URL)
    #results=[]
    list_of_links=[]
    for i in range(1,end+1):
        New_URL=URL+str(i)
        web=requests.get(New_URL)
        soup=BeautifulSoup(web.text, 'html.parser')
        results=soup.find_all('a', attrs={'class':'offer-title__link'})
        #print(results[0])   
        for result in results:
            list_of_links.append(result.get("href"))
    return list_of_links
def get_data_from_offer(URL):
    #ToDo:
    #Cleaning data
    """
    Function returns a dictionary with information about the car
    -----
    URL - (string) URL adress 
    """
    keys=['Saler','Production Year','Milage','Transmition','Quantity of doors',
    'Color', 'Invoice','Country of origin', 'accident-free','serviced in aso', 'First Registration','Polish Registration',
    'First owner','alloy wheels','description']
    info_dict=dict(dict(zip(keys,zeros(len(keys)))))
    web=requests.get(URL)
    soup=BeautifulSoup(web.text, 'html.parser')
    results_vin_accessories=str(soup.find_all('li', attrs={'class':'offer-params__item'})).split('\n')
    print(results_vin_accessories)
    try:
        info_dict['Saler']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Oferta od</span>')+3]
    except:
        info_dict['Saler']='NaN'
    try:
        info_dict['Production Year']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Rok produkcji</span>')+2]
    except:
        info_dict['Production Year']='NaN'
    try:
        info_dict['Milage']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Przebieg</span>')+3]
    except:
        info_dict['Milage']='NaN'
    try:
        info_dict['Transmition']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Skrzynia biegów</span>')+3]
    except:
        info_dict['Transmition']='NaN'
    try:
        info_dict['Quantity of doors']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Liczba drzwi</span>')+2]
    except:
        info_dict['Quantity of doors']='NaN'
    try:
        info_dict['Color']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Kolor</span>')+3]
    except:
        info_dict['Color']='NaN'
    try:
        info_dict['Invoice']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">VAT marża</span>')+3]
    except:
        info_dict['Invoice']='NaN'
    try:
        info_dict['Country of origin']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Kraj pochodzenia</span>')+3]
    except:
        info_dict['Country of origin']='NaN'
    try:
        info_dict['accident-free']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Bezwypadkowy</span>')+3]
    except:
        info_dict['accident-free']='NaN'
    try:
        info_dict['serviced in aso']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Serwisowany w ASO</span>')+3]
    except:
        info_dict['serviced in aso']='NaN'
    try:
        info_dict['First Registration']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Pierwsza rejestracja</span>')+3]
    except:
        info_dict['First Registration']='NaN'
    try:
        info_dict['Polish Registration']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Zarejestrowany w Polsce</span>')+3]
    except:
        info_dict['Polish Registration']='NaN'
    try:
        info_dict['First owner']=results_vin_accessories[results_vin_accessories.index(
            '<span class="offer-params__label">Pierwszy właściciel</span>')+3]
    except:
        info_dict['First owner']='NaN'
    #Moze byc problem z alusami
    #info_dict['alloy wheels']=results_vin_accessories[results_vin_accessories.index('<span class="offer-params__label">Pierwsza rejestracja</span>')]
       #dokończyć pobieranie reszty danych


    print(info_dict)
    #results_accessory=soup.find_all('div', attrs={'class':'offer-features__row'})
    results_description=soup.find_all('div',attrs={'class':'offer-description__description'})
    #info_dict['description']=results_description[results_description.index(<div class="offer-description__description" data-read-more="" data-text="Pokaż&nbsp;pełny opis" data-hide-text="Ukryj opis" data-readmore="" aria-expanded="false" id="rmjs-1" style="max-height: none; height: 520px;">
 
     
    return info_dict

URL='https://www.otomoto.pl/osobowe/toyota/aygo/?search%5Bfilter_enum_generation%5D%5B0%5D=gen-i-2005-2014&search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Bfilter_enum_gearbox%5D%5B0%5D=manual&search%5Bfilter_enum_gearbox%5D%5B1%5D=manual-sequential&search%5Bfilter_enum_damaged%5D=0&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=1&page='
#cars_basic=get_details_from_offer_item_wraper(URL)
#cars_basic.to_csv("Toyota_aygo_I.csv", index=False)
links_to_all_cars=get_links_to_offers(URL)
car_info=get_data_from_offer(links_to_all_cars[0])

#print("quantity of elements: {}\nelements:\n{}".format(len(links_to_all_cars),links_to_all_cars))