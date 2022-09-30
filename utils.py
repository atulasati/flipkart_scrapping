
import time
import datetime
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import TimeoutException

def get_title(driver, thread_arg):
    title = ""
    try:
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # get_title = soup.find('span',attrs={'class':'B_NuCI'})
        # title = get_title.text
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find('span',attrs={'class':'G6XhRU'}).text
        print("title :- ", title)
        if not title:
            title = driver.find_element(By.CLASS_NAME, 'B_NuCI').text
            print("title :- ", title)
        thread_arg[0] = title    

    except:
        title = driver.find_element(By.CLASS_NAME, 'B_NuCI').text
        print("title :- ", title)
        thread_arg[0] = title    
        print("Exception title :- ", thread_arg[0])
    return thread_arg

def get_mrp(driver, thread_arg):    
    mrp = ""
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        mrp = soup.find('div',attrs={'class':'_3I9_wc _2p6lqe'}).text   
        print("M.R.P. :- ", mrp)
        thread_arg[0] = mrp              
    except Exception as err:        
        print("Exception M.R.P. :- ", mrp)
        print("err:", err)
        thread_arg[0] = "" 
    return thread_arg

def get_price(driver, thread_arg):
    price = ""
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        price = soup.find('div',attrs={'class':'_30jeq3 _16Jk6d'}).text 
        print("Price :- ", price)
        thread_arg[0] = price              
    except Exception as err:        
        print("Exception Price :- ", price)
        print("err:", err)
        thread_arg[0] = ""       
    
    return thread_arg

def get_product_details(driver, thread_arg):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    brand, bullet1, bullet2, bullet3, color, touchscreen, in_the_box, model_number, touchscreen, model_name, size, pack_of = [""]*12
    try:
        
        # img_lists = soup.find('img',attrs={'class':'_2r_T1I _396QI4'}).get('src')     
        # print("img_list :- ", img_lists)    
        
        try:
            brand=driver.find_element(By.CLASS_NAME,"B_NuCI").text
            if brand:
                brand = brand.split(" ")[0]
                print("Brand:- ", brand)
        except:
            print("exception in brand")
            pass

        try:
            bullet1=driver.find_element(By.CLASS_NAME,'_2418kt').text
            print("bullet1:- ", bullet1)
        except:
            print("exception in bullet1")
            pass
        try:
            bullet2=driver.find_element(By.CLASS_NAME,'_250Jnj').text
            print("bullet2:- ", bullet2)
        except:
            print("exception in bullet2")
            pass
        try:
            bullet3=driver.find_element(By.CLASS_NAME,'xDHSrl').text
            print("bullet3:- ", bullet3) 
        except:
            print("exception in bullet3")
            pass    
        
        try:   
            table = soup.find("table", { "class" : "_14cfVK" })
            # print('table = ',table)                
            table = pd.read_html(str(table))       
            for field, value in zip(table[0][0], table[0][1]):            
                    if not in_the_box and "In The Box" == field :
                        in_the_box = value
                        print("In The Box:- ", in_the_box)
                    if not model_number and "Model Number" == field :
                        model_number = value
                        print("Model Number:- ", model_number)      
                    if not model_name and "Model Name" in field:
                        model_name = value
                        print("Model Name; ", model_name)
                    if not color and "Color" == field :
                        color = value
                        print("Color:- ", color)
                    if not touchscreen and "Touchscreen" == field :
                        touchscreen = value
                        print("Touchscreen:- ", touchscreen)
                    
        except Exception as e:
            print(e)
            pass
        # print(in_the_box,model_number,model_name,color,touchscreen)
        try:
            details1 = soup.find('div',attrs={'class':'X3BRps'}).find_all('div', attrs={'class':'col col-3-12 _2H87wv'})
            details2 = soup.find('div',attrs={'class':'X3BRps'}).find_all('div', attrs={'class':'col col-9-12 _2vZqPX'})
            for field, value in zip(details1, details2):
                # print({field.text:value.text})
                if not model_number and "Model Number" in field :
                    model_number = value.text
                    print("Model Number:- ", model_number)
                if not size and "Size" in field :
                    size = value.text
                    print("Size:- ", size)
                if not pack_of and "Pack of" in field :
                    pack_of = value.text
                    print("Pack of:- ", pack_of)            
        except Exception as e:
            print(e)
            pass
        
    except:        
        print("Exception in get product details")
    thread_arg[0] =  {
        "brand": brand,
        "bullet1": bullet1,
        "bullet2": bullet2,
        "bullet3": bullet3,
        "color": color,
        "in_the_box": in_the_box,
        "model_number": model_number,
        "model_name": model_name,
        "size": size,
        "pack_of": pack_of,
        "touchscreen": touchscreen,       
    }
    return thread_arg

def get_date():
    date = '29/09/2022 18:30:30'
    date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    max_date = date + datetime.timedelta(days=10)
    return max_date
