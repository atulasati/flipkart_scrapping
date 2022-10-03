
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
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find('span',attrs={'class':'B_NuCI'}).text
        print("title :- ", title)       
        thread_arg[0] = title
    except:       
        thread_arg[0] = ""
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

def get_brand(driver, thread_arg):
    brand = ""
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        brand = soup.find('span',attrs={'class':'G6XhRU'}).text
        print("brand :- ", brand)
        if not brand:        
            brand = soup.find('span',attrs={'class':'B_NuCI'}).tex
            brand = brand.split(" ")[0]
            print("Brand:- ", brand)
        
    except:
        brand = soup.find('span',attrs={'class':'B_NuCI'}).text
        brand = brand.split(" ")[0]
        print("brand 3 :- ", brand)
        print("exception in brand")
        pass
    thread_arg[0] = brand
    return thread_arg

def get_img_list(driver, thread_arg):
    imgs = []
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_list = soup.find_all('div',attrs={'class':'_2E1FGS'})
        if not img_list:
            img_list = soup.find_all('div',attrs={'class':'_312yBx SFzpgZ'})

        for img in img_list:
            img = img.find('img')['src'].replace('e/128', 'e/720').replace('0/128', '0/640')
            imgs.append(img)
    except Exception as er:
        print("Exception:- ", er)
        pass
    thread_arg[0] = (imgs + [""]*7)[:7]
    return thread_arg

def get_features(driver, thread_arg):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bullet1, bullet2, bullet3 = [""]*3
           
    # img_lists = soup.find('img',attrs={'class':'_2r_T1I _396QI4'}).get('src')     
    # print("img_list :- ", img_lists)    
    try:
        bullet1 = driver.find_element(By.CLASS_NAME,'_2418kt').text
        print("bullet1:- ", bullet1)
    except:
        print("exception in bullet1")
        pass
    try:
        bullet2 = driver.find_element(By.CLASS_NAME,'_1iWRKW').text
        if bullet2:
            bullet2 = bullet2.split("View more")[0]
        print("bullet2:- ", bullet2)
    except:
        print("exception in bullet2")
        pass
    try:
        bullet3 = driver.find_element(By.CLASS_NAME,'xDHSrl').text
        print("bullet3:- ", bullet3) 
    except:
        print("exception in bullet3")
        pass
    thread_arg[0] =  {        
        "bullet1": bullet1,
        "bullet2": bullet2,
        "bullet3": bullet3,
    }
    return thread_arg

def get_product_details(driver, thread_arg):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    color, in_the_box, model_number, touchscreen, model_name, size, pack_of = [""]*7
    style_code, closure, fit, fabric, pattern, reversible, collar, fabric_care, suitable_for, hem, other_details, outer_material, ideal_for, occasion, secondary_color, sole_material, season, care_instructions, headphone_type, sales_package, connectivity = [""]*21
           
    # img_lists = soup.find('img',attrs={'class':'_2r_T1I _396QI4'}).get('src')     
    # print("img_list :- ", img_lists)    
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

            if not headphone_type and "Headphone Type" == field :
                headphone_type = value
                print("Headphone Type:- ", headphone_type)
            if not sales_package and "Sales Package" == field :
                sales_package = value
                print("Sales Package:- ", sales_package)
            if not connectivity and "Connectivity" == field :
                connectivity = value
                print("Connectivity:- ", connectivity)                
    except Exception as er:
        print("Exception product table :- ", er)
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
            if not style_code and "Style Code" in field :
                style_code = value.text
                print("Style Code:- ",style_code)
            if not closure and "Closure" in field :
                closure = value.text
                print("Closure:- ",closure)
            if not fit and "Fit" in field :
                fit = value.text
                print("Fit:- ",fit)
            if not fabric and "Fabric" in field :
                fabric = value.text
                print("Fabric:- ",fabric)
            if not pattern and "Pattern" in field : 
                pattern = value.text
                print("Pattern:- ",pattern)
            if not reversible and "Reversible" in field :
                reversible = value.text
                print("Reversible:- ",reversible)
            if not collar and "Collar" in field :
                collar = value.text
                print("Collar:- ",collar)
            if not color and "Color" in field :
                color = value.text
                print("Color:- ",color)
            if not fabric_care and "Fabric Care" in field :
                fabric_care = value.text
                print("Fabric Care:- ",fabric_care)
            if not suitable_for and "Suitable For" in field :
                suitable_for = value.text
                print("Suitable For:- ",suitable_for)
            if not hem and "Hem" in field :
                hem = value.text
                print("Hem:- ",hem)
            if not other_details and "Other Details" in field :
                other_details = value.text
                print("Other Details:- ",other_details)
            if not outer_material and "Outer material "in field :
                outer_material = value.text
                print("Outer material:- ",outer_material)
            if not model_name and "Model name " in field :
                model_name = value.text
                print("Model name:- ",model_name)
            if not ideal_for and 'Ideal for ' in field :
                ideal_for = value.text
                print("Ideal for:- ",ideal_for)
            if not occasion and "Occasion " in field :
                occasion = value.text
                print("Occasion:- ",occasion)
            if not secondary_color and "Secondary color " in field :
                secondary_color = value.text
                print("Secondary color:- ",secondary_color)
            if not sole_material and "Sole material" in field :
                sole_material = value.text
                print("Sole material:- ",sole_material)
            if not season and "Season" in field:
                season = value.text
                print("Season:- ",season)
            if not care_instructions and "Care instructions " in field :
                care_instructions = value.text
                print("Care instructions:-",care_instructions)                    
    except Exception as er:
        print("Exception in product list :- ", er)
        pass    
    thread_arg[0] =  {
        "color": color,
        "in_the_box": in_the_box,
        "model_number": model_number,
        "model_name": model_name,
        "size": size,
        "pack_of": pack_of,
        "touchscreen": touchscreen,
        "style_code" : style_code,
        "closure" : closure,
        "fit" : fit,
        "fabric" : fabric,
        "pattern" : pattern,
        "reversible" : reversible,
        "collar" : collar,
        "fabric_care" : fabric_care,
        "suitable_for" : suitable_for,
        "hem" : hem,
        "other_details" : other_details,
        "outer_material" : outer_material,
        "ideal_for" : ideal_for,
        "occasion" : occasion,
        "secondary_color" : secondary_color,
        "sole_material" : sole_material,
        "season" : season,
        "care_instructions" : care_instructions,
        "headphone_type" : headphone_type,
        "sales_package" : sales_package,
        "connectivity" : connectivity,
    }
    return thread_arg

def get_date():
    date = '03/10/2022 18:30:30'
    date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    max_date = date + datetime.timedelta(days=5)
    return max_date
