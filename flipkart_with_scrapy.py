import os
import shutil
import datetime
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import filedialog
from scrapy.utils.project import get_project_settings

import json
import scrapy
import requests
import subprocess
import pandas as pd
from scrapy import Selector
from scrapy import Item, Field
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess


folders = os.listdir(".")
for folder in folders:
    if folder == "data.json":
        os.remove(folder)

r, w = os.pipe()

settings = get_project_settings()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class FlipkartItem(Item):
    fsin = Field()
    title = Field()
    mapping = Field()
    product_dsc = Field()
    brand = Field()
    mrp = Field()
    price = Field()
    # product_details = Field()
    # description = Field()
    img_urls = Field()
    Bullet_Point_1 = Field()
    Bullet_Point_2 = Field()
    Bullet_Point_3 = Field()
    Bullet_Point_4 = Field()
    Bullet_Point_5 = Field()

    # seller = Field()
    warranty = Field()
    size = Field()
    pack_of = Field()
    model_name = Field()
    color = Field()
    pattern = Field()
    model_number = Field()
    ideal_for = Field()
    sleeve_type = Field()
    country_of_origin = Field()
    neck = Field()
    fit = Field()
    width = Field()
    weight = Field()
    height = Field()
    mapping = Field()
    #for images
    image1 = Field()
    image2 = Field()
    image3 = Field()
    image4 = Field()
    image5 = Field()
    image6 = Field()
    image7 = Field()
    image8 = Field()
    image9 = Field()
    image10 = Field()    

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart_spider'
    allowed_domains = ['flipkart.com']
    data = []

    def start_requests(self):
        fsin = pd.read_excel('FSN_id.xlsx')

        for id in fsin['given_fsn']:
            yield scrapy.Request(f"https://www.flipkart.com/product/p/item?pid={id}", callback=self.new_parsing_method)

    def new_parsing_method(self, response):
        reward = FlipkartItem()
        # self.start_requests()

        reward['fsin'] = response.url.split("=")[1]
        pro_dsc, size, pack_of, brand, model_name, ideal_for, country_of_origin, model_number, material, color, pattern, sleeve_type, length, width, height, weight, fit, neck, width, weight, height, warranty = [""]*22

        try: reward['title'] = response.xpath('//span[@class="B_NuCI"]/text()').get()
        except: reward['title'] = 'null'

        try: 
            pro_dsc = response.xpath('//div[@class="_1mXcCf RmoJUa"]/p/text()').get()
            if not pro_dsc:
                pro_dsc = response.xpath('//div[@class="_1mXcCf RmoJUa"]/text()').get()
                if not pro_dsc:
                    pro_dsc = description = response.xpath('//div[@class="_1AN87F"]/text()').get()
            reward['product_dsc'] = pro_dsc
        except: 
            pass
        reward['product_dsc'] = pro_dsc

        try:
            brand = response.xpath('//span[@class="G6XhRU"]/text()').get()
            brand = brand.split("\xa0")[0]
            print("Brand 1:- ", brand)
            if not brand:
                brand = response.xpath('//span[@class="B_NuCI"]/text()').get()
                brand = brand.split(" ")[0]
                print("Brand 2:- ", brand)
        except:
            brand = response.xpath('//span[@class="B_NuCI"]/text()').get()
            brand = brand.split(" ")[0]
            print("brand 3 :- ", brand)
            print("exception in brand")
            pass
        reward['brand'] = brand
        
        try: 
            mapping = response.xpath('//a[@class="_2whKao"]/text()').extract()
            reward['mapping'] = ">".join(mapping)
        except:
            reward['mapping'] = 'null'
        
        try: reward['mrp'] = response.xpath('//div[@class="_30jeq3 _16Jk6d"]/text()').get()
        except : reward['mrp'] = 'null'

        try: reward['price'] = response.xpath('//div[@class="_3I9_wc _2p6lqe"]/text()').extract()[-1]
        except: reward['price'] = 'null'

        # self.get_product_details(response):
        
        product_keys = response.xpath('//td[@class="_1hKmbr col col-3-12"]/text()').extract()
        product_values = response.xpath('//td[@class="URwL2w col col-9-12"]/ul/li/text()').extract()

        if len(product_keys) == 0 and len(product_values) == 0:
            product_keys = response.xpath('//div[@class="col col-3-12 _2H87wv"]/text()').extract()
            product_values = response.xpath('//div[@class="col col-9-12 _2vZqPX"]/text()').extract()
        
        # products = {}
        for key,value in zip(product_keys, product_values):
            # products[key] = value
            if not size and "size" in key.lower():
                size = value
                print("Size:- ", size)
            if not pack_of and "pack of" in key.lower():
                pack_of = value
                print("Pack of:- ", pack_of)
            if not model_name and "model name" in key.lower():
                model_name = value
                print("Model Name; ", model_name)
            if not color and "color" in key.lower():
                color = value
                print("Color:- ", color)
            if not pattern and "pattern" in key.lower():
                pattern = value
                print("Pattern:- ", pattern)
            if not model_number and "model number" in key.lower():
                model_number = value
                print("Model Number:- ", model_number)
            if not ideal_for and 'ideal for ' in key.lower():
                ideal_for = value
                print("Ideal for:- ", ideal_for)
            if not sleeve_type and "sleeve" in key.lower():
                sleeve_type = value
                print("Sleeve:- ", sleeve_type)
            if not country_of_origin and "country of origin" in key.lower():
                country_of_origin = value
                print("Country of Origin:- ", country_of_origin)
            if not neck and "neck" in key.lower():
                neck = value
                print("Neck:- ", neck)
            if not fit and "fit" in key.lower():
                fit = value
                print("Fit:- ", fit)
            if not width and "width" in key.lower():
                width = value
                print("Width:- ", width)
            if not weight and "weight" in key.lower():
                weight = value
                print("weight:- ", weight)
            if not height and "height" in key.lower():
                height = value
                print("Height:- ", height)
            if not warranty and "warranty period" in key.lower():
                warranty = value
                print("Warranty:- ", warranty)


        reward['size'] = size
        reward['pack_of'] = pack_of
        reward['model_name'] = model_name
        reward['color'] = color
        reward['pattern'] = pattern
        reward['model_number'] = model_number
        reward['ideal_for'] = ideal_for
        reward['sleeve_type'] = sleeve_type
        reward['country_of_origin'] = country_of_origin
        reward['neck'] = neck
        reward['fit'] = fit
        reward['width'] = width
        reward['weight'] = weight
        reward['height'] = height
        


        imgs = []
        try:
            img_list = response.xpath('//div[@class="_2E1FGS"]/img/@src').extract()

            if len(img_list) == 0:
                img_list = response.xpath('//div[@class="_312yBx SFzpgZ"]/img/@src').extract()
                if len(img_list) == 0:
                    img_list = response.xpath('//div[@class="_2E1FGS _2_B7hD"]/img/@src').extract()

            for i, img in enumerate(img_list[:10]):
                imgs.append(img.replace('e/128', 'e/720').replace('0/128', '0/640').replace('/0/0/', '/720/640/'))

            for i in range(1,11):
                l = len(imgs)
                if i<l:
                    reward[f"image{i}"] = imgs[i]
                else:
                    reward[f"image{i}"] = 'null'
        except:
            for i in range(1,11):                
                reward[f"image{i}"] = 'null'
                   

        # description = response.xpath('//div[@class="_1mXcCf RmoJUa"]/text()').get()
        # try:
        #     if len(description) == 0:
        #         description = response.xpath('//div[@class="_1AN87F"]/text()').get()
        # except: pass
        # reward['description'] = description

        
        try: reward['Bullet_Point_1'] = response.xpath('//div[@class="_2418kt"]/ul/li/text()').extract()
        
        except: reward['Bullet_Point_1'] = 'null'
            
        try: reward['Bullet_Point_2'] = response.xpath('//div[@class="_1RLviY"]/span/span/text()').extract()
         
        except: reward['Bullet_Point_2'] = 'null'
    
        try: reward['Bullet_Point_3'] = response.xpath('//div[@class = "_2MJMLX"]/text()').extract()
        except: reward['Bullet_Point_3'] = 'null'

        try: reward['Bullet_Point_4'] = 'null'
        except: reward['Bullet_Point_4'] = 'null'

        try: reward['Bullet_Point_5'] = 'null'
        except: reward['Bullet_Point_5'] = 'null'

        try:
            if not warranty:
                warranty = response.xpath('//div[@class="_2MJMLX"]/text()').get()
        except: pass
        
        reward['warranty'] = warranty

        # print(reward.values)
        return reward

class MailSendHandler():
    def __init__(self,asin_file, root):       
        self.asin_file = asin_file      
        self.root = root
        self.output_file_name = ""
        self.dump_file_name = ""
        self.MAX_RECORDS = 0
        self.buttonClicked  = False
        self.inputfile = False
        
    def initialize(self):
        self.root.geometry('700x600+0+0')
        self.root.columnconfigure(0, weight=1)
        self.root.configure(bg='cornflower blue')
        self.root.rowconfigure(0, weight=1)
        self.tab_parent = ttk.Notebook(self.root)        
        self.tab_parent.pack(pady=10, expand=True)
        self.tab_parent.grid(row=0, column=0, sticky='nsew')       
        self.tab1 = tk.Frame(self.tab_parent, bg='#ccffcc')
        self.tab1.pack(fill='both', expand=True)
        self.tab_parent.add(self.tab1, text="Flipkart Product Scraping by FSN")       
        self.ButtonFont = font.Font(family='Helvetica', size=10, weight='bold')
        self.SubmitButtonFont = font.Font(family='Helvetica', size=11, weight='bold',underline=1)
        # === WIDGETS FOR TAB ONE
        self.files = LabelFrame(self.tab1, text='Fils Attachment', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
        self.files.grid(row=0, column=0, columnspan=2, sticky=W, padx=25, pady=25)        
        self.asinFileButton = tk.Button(self.files, text="Browse asin File:", width=18, compound="c", bg='cornflower blue', fg='#ffffff', command=self.get_asin_file)

        self.options = [10,20,50,100,200,300,500]
        self.clicked = StringVar()
        self.clicked.set( "Select Total number of FSN-ID" )
        self.drop = OptionMenu(self.files , self.clicked , *self.options)
        MAX_RECORDS = str(self.clicked.get())

        self.drop.grid(row=0, column=1, columnspan=2, sticky=W, padx=15, pady=25)
        self.asinFileButton['font'] = self.ButtonFont   

        self.SendButton = tk.Button(self.files, text="SUBMIT", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.run_spider)        
        self.SendButton['font'] = self.SubmitButtonFont
        
            

        
        # === ADD WIDGETS TO GRID ON TAB ONE        
        self.asinFileButton.grid(row=0, column=0, padx=20, pady=20)       
        self.SendButton.grid(row=1, column=0, padx=5, pady=15)        
        # self.tab_parent.pack(expand=3, fill='both')
              

        root.mainloop()        
  
    def get_asin_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
        if file:
            self.files = LabelFrame(self.tab1, text='Info', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
            self.files.grid(row=5, column=0, columnspan=1, sticky=W, padx=15, pady=20)
            self.asinFileLabel = tk.Label(self.files, text= file.name, font='Courier 9 bold', width=80, height=2, anchor="w")
            self.asinFileLabel.grid(row=0, column=1, padx=15, pady=15)
            self.asinFileLabel.pack()
            self.asin_file = file.name

            if(self.asin_file.split(".")[-1] == 'xlsx'):
                # date = utils.get_date()
                # if datetime.datetime.now() > date: raise Exception
                df = pd.read_excel(self.asin_file)
                # try:
                #     # if os.path.isdir(ROOT_DIR+'/tmp'):
                #     #     shutil.rmtree(ROOT_DIR+'/tmp')
                #     if f'{os.path.join(os.getcwd())}\\FSN_id.xlsx':    
                # except: pass  
                # os.makedirs(ROOT_DIR+'/tmp')
                df.to_excel(os.path.join(os.getcwd(), "FSN_id.xlsx"), index = False)
                self.inputfile = True
            else:
                messagebox.showerror("Error", "Open .xlsx file only")
                self.inputfile = False
        else:           
            messagebox.showerror("Error", "Unable to open FSN file")
            self.inputfile = False
        return self.asin_file

    def get_date(self):
        date = '06/10/2022 18:30:30'
        date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        max_date = date + datetime.timedelta(days=7)
        return max_date
    
    def scrape(self):        
        if self.buttonClicked == False:            
            process = CrawlerProcess(settings={
                "FEEDS": {
                    "data.json": {"format": "json"},
                },
            })
            process.crawl(FlipkartSpider)
            process.start()
            self.get_scraping_file()
        else:
            messagebox.showerror("Error", "For next Input file please restart 'Flipkart_Product' application")
            self.root.destroy()

    def run_spider(self):
        if datetime.datetime.now() > self.get_date(): raise Exception
        if self.inputfile == False:
            messagebox.showerror("Error", "Please First Input FSN file then click on SUBMIT")
            return
        self.scrape()

        self.files = LabelFrame(self.tab1, text='Open Scrapped file', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
        self.files.grid(row=8, column=0, columnspan=1, sticky=W, padx=20, pady=20)
        self.scrapingFileButton = tk.Button(self.files, text="OPEN:", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.show_excel)

        self.scrapingFileButton['font'] = self.SubmitButtonFont
        self.scrapingFileButton.grid(row=0, column=0, padx=20, pady=20)
        
        print("excel file creation done")
        messagebox.showinfo("Success", f"Amozon Product Scraping Done!")        
        self.buttonClicked = not self.buttonClicked
        print("self.buttonClicked:- ", self.buttonClicked)
        


    # def call_subprocess_command(self):
    #     """
    #     Call the subprocess command fo call scrapy
    #     :return:
    #     """
    #     subprocess.run('scrapy crawl flipkart_spider -o tmp/data.json')
    
    def get_scraping_file(self):
        self.output_file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.xlsx'
        # print('Root Dir:', ROOT_DIR)
        
        pd.read_json(f'{os.path.join(os.getcwd())}\\data.json').to_excel(os.path.join(os.getcwd(),self.output_file_name),index = False)
        print("output_file_name :-",self.output_file_name)

        all_files = os.listdir(".")
        for files in all_files:
            if files == "data.json":
                os.remove(files)
        
        file_path = os.getcwd()
        file = file_path+ "//" + self.output_file_name
        self.file_path = file
        self.asinFileLabel["text"]= f"Out file is available now at {file})"
        self.root.update()     

    def open_scrape_file(self):
        self.files = LabelFrame(self.tab1, text='Open Scrapped file', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
        self.files.grid(row=8, column=0, columnspan=1, sticky=W, padx=20, pady=20)
        self.scrapingFileButton = tk.Button(self.files, text="OPEN:", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.show_excel)

        self.scrapingFileButton['font'] = self.SubmitButtonFont
        self.scrapingFileButton.grid(row=0, column=0, padx=20, pady=20)
        
        print("excel file creation done")
        messagebox.showinfo("Success", f"Amozon Product Scraping Done!")
        
    
    def show_excel(self): 
        try:
            os.system('"%s"' %self.file_path)
            print("Excel file opened")            
        except:          
            messagebox.showerror("Error", "Unable to open file")

if __name__ == "__main__":    
    try:
        asin_file = ""    
        root = tk.Tk()
        s = ttk.Style(root)     
        s.theme_create( "MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": 'snow'} },
            "TNotebook.Tab": {"configure": {"padding": [100, 10], "background": 'snow',
                                            "font" : ('Arial', '12', 'bold')},}})
        s.theme_use("MyStyle")    
        s.map('TNotebook.Tab', background=[('selected', '#ccffcc')])
        # date = utils.get_date()
        #  ifdatetime.datetime.now() > date: raise Exception
        root.title("Flipkart Product")
        mailSendHandler = MailSendHandler(asin_file, root)
        mailSendHandler.initialize()
    except: print('END')