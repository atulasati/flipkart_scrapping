import os
import main
import utils
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
        self.SendButton = tk.Button(self.files, text="SUBMIT", width=12, compound="c", bg='cornflower blue', fg='#ffffff', command=self.send_function)        
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
        else:           
            messagebox.showerror("Error", "Unable to open asin file")   

    def send_function(self):     
        # code for send button function
        dict_list = []
        dict_skip = []
        dict_s = {}
        self.MAX_RECORDS = int(self.clicked.get())
        print("MAX_RECORDS:- --", self.MAX_RECORDS)
        try:
            if(self.asin_file.split(".")[-1] == 'xlsx'):
                date = utils.get_date()
                if datetime.datetime.now() > date: raise Exception
                df = pd.read_excel(self.asin_file)
                print(df["given_fsn"])
                for i, value in enumerate(df["given_fsn"][:self.MAX_RECORDS]):
                    given_fsn = value
                    # if i>=2:break
                    # given_fsn = "B08XXY9SP8"
                    di = main.get_product_value(given_fsn)                
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
        print("output_file_name :-",self.output_file_name)
        file_path = os.getcwd()
        file = file_path+ "\\" + self.output_file_name        
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
        date = utils.get_date()
        #  ifdatetime.datetime.now() > date: raise Exception
        root.title("Amazon Product")
        mailSendHandler = MailSendHandler(asin_file, root, 2)
        mailSendHandler.initialize()
    except: print('END')