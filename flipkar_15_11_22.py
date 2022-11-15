import os
import json
import utils
import scrapy
import datetime
import pandas as pd
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import filedialog
from scrapy import Item, Field
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


folders = os.listdir(".")
for folder in folders:
    if folder == "data.json":
        os.remove(folder)

r, w = os.pipe()

settings = get_project_settings()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart_spider'
    allowed_domains = ['flipkart.com']
    data = []

    def start_requests(self):
        fsin = pd.read_excel('FSN_id.xlsx')

        for id in fsin['given_fsn']:
            yield scrapy.Request(f"https://www.flipkart.com/product/p/item?pid={id}", callback=self.new_parsing_method)

    def new_parsing_method(self, response):
        main_list = []
        reward = utils.get_product_data(response)
        main_list.append(reward)
        print('--------------------------------------------------main list---------------------------')
        print(main_list)

        return main_list

class MailSendHandler():
    def __init__(self,asin_file, root):       
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
                df = pd.read_excel(self.asin_file)
                df.to_excel(os.path.join(os.getcwd(), "FSN_id.xlsx"), index = False)
            else:
                messagebox.showerror("Error", "Open .xlsx file only")
        else:           
            messagebox.showerror("Error", "Unable to open asin file")
        return self.asin_file

    def get_date(self):
        date = '01/11/2022 18:30:30'
        date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        max_date = date + datetime.timedelta(days=30)
        return max_date
    
    def scrape(self):
        process = CrawlerProcess(settings={
            "FEEDS": {
                "data.json": {"format": "json"},
            },
        })
        process.crawl(FlipkartSpider)
        process.start()

        self.get_scraping_file()

    def run_spider(self):
        if datetime.datetime.now() > self.get_date(): raise Exception

        self.scrape()

        self.files = LabelFrame(self.tab1, text='Open Scrapped file', font=('Arial', '12', 'bold'), bd=5, relief=RIDGE)
        self.files.grid(row=8, column=0, columnspan=1, sticky=W, padx=20, pady=20)
        self.scrapingFileButton = tk.Button(self.files, text="OPEN:", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.show_excel)

        self.scrapingFileButton['font'] = self.SubmitButtonFont
        self.scrapingFileButton.grid(row=0, column=0, padx=20, pady=20)
        
        print("excel file creation done")
        messagebox.showinfo("Success", f"Amozon Product Scraping Done!")
    
    def get_scraping_file(self):
        self.output_file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.xlsx'
        # print('Root Dir:', ROOT_DIR)
        
        pd.read_json(f'{os.path.join(os.getcwd())}//data.json').to_excel(os.path.join(os.getcwd(),self.output_file_name),index = False)
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
        root.title("Flipkart Product")
        mailSendHandler = MailSendHandler(asin_file, root)
        mailSendHandler.initialize()
    except: print('END')