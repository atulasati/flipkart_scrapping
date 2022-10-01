import os
import sys
import time
import utils
import random
import datetime
import threading
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

def get_product_value(fsn):    
    options = Options()
    options.add_argument("no-sandbox")
    options.add_argument("headless")
    options.add_argument("--log-level=3")
    options.add_argument("start-maximized")
    options.add_argument("window-size=1900,1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    
    if fsn:
        print(f"\n\n START for ASIN: {fsn}")
        dict_ = {}
        title, mrp, price, img_src_list = "", "", "", ""
              
        url = f"https://www.flipkart.com/product/p/item?pid={fsn}"
        date = utils.get_date()

        try:
            print("\n\n\tFSN :",fsn)
            dict_["fsn"] = fsn
            driver.get(url)
            time.sleep(3)
            print(url)
            
            get_title = [None] * 2
            get_brand = [None] * 2
            get_mrp  = [None] * 2
            get_price  = [None] * 2
            get_features = [None] * 2
            get_product_details  = [None] * 2
            get_img_list = [None] * 2          
        
            thread_1 = threading.Thread(target= utils.get_title ,args=(driver,get_title) ,name='thread_1')
            thread_2 = threading.Thread(target= utils.get_brand ,args=(driver,get_brand) ,name='thread_2')
            thread_3 = threading.Thread(target= utils.get_mrp ,args=(driver,get_mrp) ,name='thread_3')
            thread_4 = threading.Thread(target= utils.get_price ,args=(driver,get_price) ,name='thread_4')
            thread_5 = threading.Thread(target= utils.get_img_list ,args=(driver,get_img_list) ,name='thread_5')
            thread_6 = threading.Thread(target= utils.get_features ,args=(driver,get_features) ,name='thread_6')
            thread_7 = threading.Thread(target= utils.get_product_details ,args=(driver,get_product_details) ,name='thread_7')
           
            thread_1.start()
            thread_2.start()
            thread_3.start()
            thread_4.start()
            thread_5.start()
            thread_6.start()
            thread_7.start()            

            thread_1.join()
            thread_2.join()
            thread_3.join()
            thread_4.join()
            thread_5.join()
            thread_6.join()
            thread_7.join()


            title = get_title[0]
            print("\n\n\tTITLE :",title)
            if not title:
                return 0
            dict_["Product Title"] = title

            brand = get_brand[0]
            print("\n\n\tBRAND :",brand)            
            dict_["Brand"] = brand

            mrp = get_mrp[0]
            print("\n\n\tMRP:- ", mrp)
            dict_["M.R.P."] = mrp    
            
            price = get_price[0]
            print("\n\n\tPrice:- ", price)
            dict_["Price"] = price

            if (dict_["M.R.P."] is None or dict_["M.R.P."] == '')  and (dict_["Price"] is None or dict_["Price"] == ''):
                try:
                    availibility = driver.find_element(By.ID, 'availability')
                    if availibility:
                        dict_["M.R.P."] = 'Currently Unavailable'
                        dict_["Price"] = 'Currently Unavailable'
                except:
                    dict_["M.R.P."] = 'FSN Blocked, Retry Again'
                    dict_["Price"] = 'FSN Blocked, Retry Again'
                    pass

            img_src_list = get_img_list[0]
            print("\n\n\tLIST OF IMAGES :\n", img_src_list)
            for i in range(len(img_src_list)):
                dict_[f"Image{i+1}"] = img_src_list[i]

            print("\n\n\FEATURES :\n\n\t", get_features[0])
            dict_.update(get_features[0])
            
            print("\n\n\tDETAILS :\n\n\t", get_product_details[0])
            dict_.update(get_product_details[0])            
    
        except:
            print("fsn :", fsn)
            print("    ", traceback.format_exc())
            driver.close()
            return (dict_)  

        print("\n\n\tRESULT:-\n\n\t",dict_)
        if not dict:
            print('Dictionary Empty')                 
        driver.close()
            
    return (dict_)  
   