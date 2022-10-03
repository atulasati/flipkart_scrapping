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

r, w = os.pipe()

settings = get_project_settings()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class FlipkartItem(Item):
    fsin = Field()
    title = Field()
    mrp = Field()
    price = Field()
    product_details = Field()
    description = Field()
    img_urls = Field()
    Bullet_Point_1 = Field()
    Bullet_Point_2 = Field()
    Bullet_Point_3 = Field()
    seller = Field()
    warranty = Field()


class FlipkartSpider(scrapy.Spider):
    name = 'flipkart_spider'
    allowed_domains = ['flipkart.com']
    data = []

    def start_requests(self):
        fsin = pd.read_excel('tmp/FSN_id.xlsx')

        for id in fsin['given_fsn']:
            yield scrapy.Request(f"https://www.flipkart.com/product/p/item?pid={id}", callback=self.new_parsing_method)

    def new_parsing_method(self, response):
        reward = FlipkartItem()
        reward['fsin'] = response.url

        try: reward['title'] = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()
        except: reward['title'] = 'null'

        try: reward['mrp'] = response.xpath('//div[@class="_30jeq3 _16Jk6d"]/text()').get()
        except : reward['mrp'] = 'null'

        try: reward['price'] = response.xpath('//div[@class="_3I9_wc _2p6lqe"]/text()').extract()[-1]
        except: reward['price'] = 'null'

        product_keys = response.xpath('//td[@class="_1hKmbr col col-3-12"]/text()').extract()
        product_values = response.xpath('//td[@class="URwL2w col col-9-12"]/ul/li/text()').extract()

        if len(product_keys) == 0 and len(product_values) == 0:
            product_keys = response.xpath('//div[@class="col col-3-12 _2H87wv"]/text()').extract()
            product_values = response.xpath('//div[@class="col col-9-12 _2vZqPX"]/text()').extract()
        
        products = {}
        for key,value in zip(product_keys, product_values):
            products[key] = value

        reward['product_details'] = products

        imgs = []
        img_list = response.xpath('//div[@class="_2E1FGS"]/img/@src').extract()

        if len(img_list) == 0:
            img_list = response.xpath('//div[@class="_312yBx SFzpgZ"]/img/@src').extract()

        for i, img in enumerate(img_list[:10]):
            imgs.append(img.replace('e/128', 'e/720').replace('0/128', '0/640'))
        
        reward['img_urls'] = imgs

        description = response.xpath('//div[@class="_1mXcCf RmoJUa"]/text()').get()
        try:
            if len(description) == 0:
                description = response.xpath('//div[@class="_1AN87F"]/text()').get()
        except: pass
        reward['description'] = description

        reward['Bullet_Point_1'] = response.xpath('//div[@class="_2418kt"]/ul/li/text()').extract()    
            
        reward['Bullet_Point_2'] = response.xpath('//div[@class="_1RLviY"]/span/span/text()').extract()
    
        reward['Bullet_Point_3'] = response.xpath('//div[@class = "_2MJMLX"]/text()').extract()

        reward['warranty'] = response.xpath('//div[@class="_2MJMLX"]/text()').get()

        # print(reward.values)
        return reward

class MailSendHandler():
    def __init__(self,asin_file, root, clickbu):       
        self.asin_file = asin_file      
        self.root = root
        self.output_file_name = ""
        self.dump_file_name = ""
        self.MAX_RECORDS = 0
        
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

        self.options = [10,50,100,200,500,700,1000]
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
                try:
                    if os.path.isdir(ROOT_DIR+'/tmp'):
                        shutil.rmtree(ROOT_DIR+'/tmp')      
                except: pass  
                os.makedirs(ROOT_DIR+'/tmp')
                df.to_excel(os.path.join(os.getcwd(), "tmp/FSN_id.xlsx"), index = False)
            else:
                messagebox.showerror("Error", "Open .xlsx file only")
        else:           
            messagebox.showerror("Error", "Unable to open asin file")
        return self.asin_file

    def scrape(self):
        process = CrawlerProcess(settings={
            "FEEDS": {
                "tmp/data.json": {"format": "json"},
            },
        })
        process.crawl(FlipkartSpider)
        process.start()

    def run_spider(self):
        self.scrape()

        self.files = LabelFrame(self.tab1, text='Open Scrapped file', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
        self.files.grid(row=8, column=0, columnspan=1, sticky=W, padx=20, pady=20)
        self.scrapingFileButton = tk.Button(self.files, text="OPEN:", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.get_scraping_file)

        self.scrapingFileButton['font'] = self.SubmitButtonFont
        self.scrapingFileButton.grid(row=0, column=0, padx=20, pady=20)
        
        print("excel file creation done")
        messagebox.showinfo("Success", f"Amozon Product Scraping Done!")


    def call_subprocess_command(self):
        """
        Call the subprocess command fo call scrapy
        :return:
        """
        subprocess.run('scrapy crawl flipkart_spider -o tmp/data.json')

    def send_function(self):     
        # code for send button function
        dict_list = []
        dict_skip = []
        dict_s = {}
        self.MAX_RECORDS = int(self.clicked.get())
        print("MAX_RECORDS:- --", self.MAX_RECORDS)
        try:
            if(self.asin_file.split(".")[-1] == 'xlsx'):
                # date = utils.get_date()
                # if datetime.datetime.now() > date: raise Exception
                df = pd.read_excel(self.asin_file)
                print(df["given_fsn"])
                for i, value in enumerate(df["given_fsn"][:self.MAX_RECORDS]):
                    given_fsn = value
                    # if i>=2:break
                    # given_fsn = "B08XXY9SP8"
                    # di = spider.FlipkartSpider.start_requests(given_fsn)                
                    print("Running Asin Id is:", given_fsn)  
                    fsnid = given_fsn
                    self.asinFileLabel["text"]= f"{i+1}) FSN-ID {fsnid} is running...."
                    self.root.update()
                    if di == 0:  
                        dict_skip.append(given_fsn)
                        continue
                    dict_ = di
                    print('========',dict_)                           
                    dict_list.append(dict_)
                    
                    if ((i+1)%100==0):        
                        df = pd.DataFrame(dict_list)
                        self.output_file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d")}.xlsx'
                        df.to_excel(os.path.join(os.getcwd(), self.output_file_name), index = False)
                        print(f"Excel file creation done for {((i+1)/100)*100} FSN-ID")
                        self.asinFileLabel["text"] = f"Excel file creation done for {((i+1)/100)*100} FSN'S ID"
                        self.root.update()                                         
                df = pd.DataFrame(dict_list)
                df2 = pd.DataFrame(columns=df.columns)
                df2['fsn'] =  dict_skip
                final_df = pd.concat([df,df2])
                print(final_df)                
                print("FSN skipping", dict_skip)
                self.output_file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.xlsx'
                final_df.to_excel(os.path.join(os.getcwd(), self.output_file_name), index = False)
                self.asinFileLabel["text"]= f"All data stored at: {os.getcwd()} / {self.output_file_name}"
                self.root.update()

                self.files = LabelFrame(self.tab1, text='Open Scrapped file', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
                self.files.grid(row=8, column=0, columnspan=1, sticky=W, padx=20, pady=20)
                self.scrapingFileButton = tk.Button(self.files, text="OPEN:", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.get_scraping_file)

                self.scrapingFileButton['font'] = self.SubmitButtonFont
                self.scrapingFileButton.grid(row=0, column=0, padx=20, pady=20)
                
                print("excel file creation done")
                messagebox.showinfo("Success", f"Amozon Product Scraping Done!")
        except Exception as err:
            print("Exception occure:- ", err)

    def get_scraping_file(self):
        self.output_file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.xlsx'
        # print('Root Dir:', ROOT_DIR)
        
        pd.read_json(ROOT_DIR+'/tmp'+'/data.json').to_excel(os.path.join(os.getcwd(), self.output_file_name),index = False)
        print("output_file_name :-",self.output_file_name)
        file_path = os.getcwd()
        file = file_path+ "//" + self.output_file_name        
        try:
            os.system('"%s"' %file)
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
        mailSendHandler = MailSendHandler(asin_file, root, 2)
        mailSendHandler.initialize()
    except: print('END')