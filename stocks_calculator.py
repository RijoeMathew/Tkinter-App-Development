'''
Name: Rijoe Chacko Mathew
Myseneca: rcmathew1
Description: Assignment 2 Final Submission - Store Stock Calculator
'''

import csv #imports the csv module
import sys #imports the sys module
import os #imports the os module
import time #imports the time module
import re
import shutil

from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from datetime import datetime

user_input="" #initalize user input with empty string
list_of_dicts_csv=[] #intialize the list of dictionary to hold the csv data
sales={} #initalize the dictionary to store the sales count of each items
lost_sales={} #initalize the dictionary to store the lost sales count of each items
stocks={} #initalize the dictionary to store the current stock count of each items
warehouse={} #initalize the dictionary to store the warehouse count of each items


class StoreStockCalculator(Frame):

    def __init__(self):        
        Frame.__init__(self)    
        self.master.title("Store Stock Calculator")
        self.grid()
        
        self._label1 = Label(self, text = "Sale Item")
        self._label1.grid(row = 1, column = 0, sticky='w', padx=20)
        self._sale_item = StringVar()    
        self._sale_item_Entry = Entry(self, textvariable= self._sale_item,justify=CENTER, relief="solid", width=30)
        self._sale_item_Entry.grid(row=1, column=1,columnspan=2)
        self._sale_item_Entry.bind('<Button-1>', self._handleEventSale)

        self._label2 = Label(self, text = "Import CSV File")
        self._label2.grid(row = 0, column = 0, sticky='w', padx=20)

        self._file_name=StringVar()
        self._file_name.set("Select a file")
        self._file_name_Entry = Entry(self, textvariable= self._file_name,justify=CENTER, relief="solid", width=30, state="readonly")        
        self._file_name_Entry.grid(row=0, column=1, pady=15)
             

        self._label3 = Label(self, text = "Export Updated Stock")
        self._label3.grid(row = 4, column = 0, sticky='w', padx=20)
        self._export_file_name = StringVar()
        self._export_file_name.set('Enter the csv file name to export')
        self._export_file_name_Entry = Entry(self, textvariable= self._export_file_name,justify=CENTER, relief="solid", width=30)
        self._export_file_name_Entry.grid(row=4, column=1)  
        self._export_file_name_Entry.bind('<FocusIn>', self._handleEventExport)


        self._label4 = Label(self, text = "Status")
        self._label4.grid(row = 5, column = 0, sticky='w', padx=20, pady=25)
        self._outputVar = StringVar()
        self._outputEntry = Entry(self, textvariable= self._outputVar,justify=CENTER, readonlybackground="#F0F0F0", fg="black", state="readonly", relief="flat", width=30)
        self._outputEntry.grid(row=5, column=1, sticky='w', pady=10)

        self._label5 = Label(self, text = "")
        self._label5.grid(row = 2, column = 1, sticky='w')


        self._button1 = Button(self, text = "Show Current Stock", command = self._show_current_stock, bg="Light Green", relief="groove")
        self._button1.grid(row = 0, column = 3, sticky='w', padx=90)

        self._button2 = Button(self, text = "Generate Reports", command = self._generate_reports, bg="Light Blue", relief="groove")
        self._button2.grid(row = 3, column = 1, sticky='w', pady=20)

        self._button3 = Button(self, text = "Add Sale", command = self._add_sale, bg="Light Green", relief="groove")
        self._button3.grid(row = 1, column = 3, sticky='w', padx=10, pady=10)

        self._button4 = Button(self, text = "Export", command = self._export_file, relief="groove", bg="Light Green")
        self._button4.grid(row = 4, column = 3, sticky='w', padx=10)

        self._button5 = Button(self, text = "Clear", command = self._clear_window, relief="groove", bg="Light Green")
        self._button5.grid(row = 5, column = 3, sticky='w', padx=10)

        self._button6 = Button(self, text = "Exit", command = self._exit_application, relief="groove", bg="Pink")
        self._button6.grid(row = 5, column = 3, sticky='w', padx=55)

        self._button7 = Button(self, text='Open a File',command=self._select_file_to_import, relief="groove", bg="Light Grey")
        self._button7.grid(row = 0, column = 3, sticky='w', padx=10)


        self._list_of_dicts_csv={}
        self._sales={}
        self._lost_sales={}
        self._stocks={}
        self._no_of_items=int()
        self._warehouse={} 
        self._file_import_selected=StringVar()
        self._file_export_selected=StringVar()
        
        

    def _select_file_to_import(self):
        filetypes = (('csv files', '*.csv'),)
        self._file_import_selected.set(fd.askopenfilename(title='Open a file',initialdir='.',filetypes=filetypes))
        if self._file_import_selected.get()!="":
            #showinfo(title='Selected File',message=self._file_import_selected.get())
            file_selected=self._file_import_selected.get()
            self._file_name.set(file_selected.split('/')[-1])    
    

    def _handleEventExport(self, event):
        self._export_file_name_Entry.delete('0', 'end')

    def _handleEventSale(self, event):
        self._sale_item_Entry.delete('0', 'end')

    def _exit_application(self):
        clr = os.system('cls')
        sys.exit(0)


    def _clear_window(self):
        clr = os.system('cls')
        self.destroy()
        StoreStockCalculator().mainloop()
        sys.exit(0)

    def _read_csv(self,file_name): #function has 1 parameter which is the file name of the csv file that is to be read and returns a value which is the list of dictionaries
        "Takes the csv file and creates a list of dictionaries"
        list_of_dicts=[] #initialises the list of dictionaries

        try:
            f = open(file_name, 'r') #creates a file object with read operation
        except FileNotFoundError: #this line gets executed if the filename provided is not found at the location
            showerror(message=f"Error! File {file_name} was not found.")
            self.destroy()
            StoreStockCalculator().mainloop()
            sys.exit(0)
            #sys.exit(1) #script execution stops        
        except PermissionError: #this line gets executed if the user has no permission to read the file
            showerror(message=f"Error! You do not have permission to open {file_name}.") #displays the error message
            self.destroy()
            StoreStockCalculator().mainloop()
            sys.exit(0)
        except: #this line gets executed if any other generic exceptions occurs
            showerror(message="Error! Something went wrong!") #displays the error message
            self.destroy()
            StoreStockCalculator().mainloop()
            sys.exit(0)
            
        reader = csv.DictReader(f)
        for row in reader: #iterates over each row in csv file
            list_of_dicts.append(row) #adds each row as a dictionary to the list of dictionaries

        f.close() #closes the file object        
        return list_of_dicts


    def _write_csv(self,list_of_dicts_1,file_name): #function has 2 parameters which is the list of dictionaries and the file name of csv file and does not return any value
        "Writes data to the csv file"
        try:
            f1 = open(file_name, 'w', newline='') #creates a file object with write operation
        except PermissionError: #this line gets executed if the user has no permission to read the file
            showerror(message=f"Error! You do not have permission to open {file_name}.") #displays the error message
            sys.exit(0)

        except: #this line gets executed if any other generic exceptions occurs
            showerror(message="Error! Something went wrong!") #displays the error message
            sys.exit(0)
        
        fieldnames = list_of_dicts_1[0].keys() #takes the keys of the first dictionary from the list of dictionaries and stores the key list in a variable
        w = csv.DictWriter(f1, fieldnames=fieldnames)
        w.writeheader() #create the header of the csv file
        for row in list_of_dicts_1: #iterates over each dictionary from the list of dictionaries
            w.writerow(row) #adds each dictionary as a row in the csv file
        f1.close() #closes the file object    


    def _show_current_stock(self):
        clr = os.system('cls')
        file_name_1=self._file_name.get()
        if file_name_1=="Select a file":
            file_name_1=""
        if file_name_1=="":
            showerror(message="Error: Please select a CSV file first", parent=self)
        else:
            if len(self._list_of_dicts_csv)==0:
                self._list_of_dicts_csv=self._read_csv(file_name_1) #calls the function to read the csv file and stores the list of dictionaries returned in a variable
                for dicts in self._list_of_dicts_csv: #iterates over each dictionary in the list of dictionaries
                    self._sales[dicts['Item']]=0 #initalises the key,values pairs in the sales dictionary
                    self._lost_sales[dicts['Item']]=0 #initalises the key,values pairs in the lost sales dictionary
                    self._stocks[dicts['Item']]=int(dicts['Current Stock']) #initalises the key,values pairs in the current stocks dictionary
                    

            stock_header=f"{'#':<4}{'Item':<15}{'Current Stock':^20}{'Price per Item':>10}" #define the header of current stock report
            stock_header_length=len(stock_header)
            print(stock_header) #display the current stock header
            print("="*stock_header_length)

            for dicts in self._list_of_dicts_csv: #iterates over each dictionary in the list of dictionaries
                item_sl_no=str(self._list_of_dicts_csv.index(dicts)+1)+'.' #stores the item serial no in a variable
                item_name=dicts['Item'] #gets the value corresponding to the key and stores the value in a variable
                stock=int(dicts['Current Stock']) #gets the value corresponding to the key and stores the value in a variable after converting to integer data type
                item_price=float(dicts['Price per Item']) #gets the value corresponding to the key and stores the value in a variable after converting to floating point data type
                item_price_formatted='$ '+f"{item_price:.2f}" #format the item price to display 2 places after decimal point
                stock_line_item=f"{item_sl_no:<4}{item_name:<15}{stock:^20}{item_price_formatted:>14}" #define the row of current stock report
                
                print(stock_line_item) #display the current stock details            

            self._outputVar.set('Current Stock List Generated!')


    def _add_sale(self):
        file_name_1=self._file_name.get()
        if file_name_1=="Select a file":
            showerror(message="Error: Please import the CSV file first before adding the sales", parent=self)
        else:
            if len(self._list_of_dicts_csv)==0:
                self._list_of_dicts_csv=self._read_csv(file_name_1)

                for dicts in self._list_of_dicts_csv: #iterates over each dictionary in the list of dictionaries
                    self._sales[dicts['Item']]=0 #initalises the key,values pairs in the sales dictionary
                    self._lost_sales[dicts['Item']]=0 #initalises the key,values pairs in the lost sales dictionary
                    self._stocks[dicts['Item']]=int(dicts['Current Stock']) #initalises the key,values pairs in the current stocks dictionary


            user_input=self._sale_item.get() #initalize user input with empty string
            self._no_of_items=len(self._list_of_dicts_csv) #calculates the total number of items in the input csv file 
            

            valid_input_list=[] #initialises the list that holds the valid list of inputs
            for i in range(1,self._no_of_items+1): #iterates over 1 till no of elements value
                valid_input_list.append(str(i)) #adds each value of i to the valid list of inputs
            

            if user_input not in valid_input_list: #checks if user has entered anything other that the valid inputs
                showerror(message='Error! Please enter a number between 1 and '+str(self._no_of_items), parent=self)
                                
                
            else: #checks if the user has not entered e
                for i in range(0,self._no_of_items): #iterates over 0 till the value of no of items    
                    if int(user_input)-1==i: #checks if user has entered the number corresponding to the ith item in the list if items
                        item_name=self._list_of_dicts_csv[i]['Item'] #gets the item name of ith item and stores it in a variable
                        self._sales[item_name]+=1 #increments the sales by 1 for the ith item
                        if self._stocks[item_name]!=0: #checks if current stock has not reached zero
                            self._stocks[item_name]-=1 #decrements current stock by 1 till it reaches 0
                        else:
                            self._lost_sales[item_name]+=1 #increments lost sale by 1 since current sale has reached 0
                        
                        if self._sales[item_name]==1:
                            sale_txt="sale"
                        else:
                            sale_txt="sales"
                        self._label5["text"] = f"{self._sales[item_name]} {sale_txt} of {item_name} added!"

                sales_str=""
                for k,y in self._sales.items():
                    sales_str+=k+' : '+str(y)+', '
                sales_str=sales_str[:-2]

                self._outputVar.set(f"{sales_str}")

    def _generate_reports(self):

        clr = os.system('cls')

        file_name_1=self._file_name.get()
        if file_name_1=="Select a file":
            showerror(message="Error: Please import the CSV file first before generating the reports", parent=self)
        else:
            #diplays the total sales report
            history_path=".\Reports History"
            history_files_list=[] #initialize the file to be copied list
            for root, directories, filenames in os.walk('.'): #os.walk method takes a target directory as its argument and returns a 3-tuple
                for files in filenames: #iterates over each file name in the file names list
                    result= re.findall(r'\bReports\w*.txt\b', files) # find all instances of the pattern in the files string and stores the results in a list
                    if result: #checks if the result list is non empty
                        history_files_list+=[files] #appends each file name to the list
                break            
            
            for files in history_files_list:
                shutil.move(files, history_path)            

            date_time = datetime.now()
            date_time_formatted=date_time.strftime("%d%m%Y_%H_%M_%S")
            file_name="Reports_"+date_time_formatted+".txt"
            f = open(file_name, 'w')
            sys.stdout = f
            print('Total Sales') #display the total sales report heading
            
            total_sales_header=f"{'#':<4}{'Item':<15}{'Sales':^20}{'Price per Item':^10}{'Total':>10}"
            total_sales_header_length=len(total_sales_header)
            print(total_sales_header)
            print("="*total_sales_header_length)

            total_sales_amt=0 #itializes the total sales amount as 0
            for i in range(0,self._no_of_items): 
                item_name=self._list_of_dicts_csv[i]['Item'] #gets the item name of the ith item and stores it in a variable
                sale=self._sales[item_name] #stores the sales of ith item in a variable
                lost_sale=self._lost_sales[item_name] #stores the lost sales of ith item in a variable
                item_price=float(self._list_of_dicts_csv[i]['Price per Item']) #gets the value corresponding to the key and stores the value in a variable after converting to floating point data type
                item_price_formatted='$ '+f"{item_price:.2f}" #format the item price to display 2 places after decimal point
                sales_total=(sale-lost_sale)*item_price #calculates the sales total of the current item
                total_sales_amt+=sales_total #increments the total sales amount with the total amount of current item
                sales_total_formatted='$ '+f"{sales_total:.2f}" #formats to to display 2 places after decimal point
                sl_no=str(i+1)+'.' #sl no of the report
                sales_line_item=f"{sl_no:<4}{item_name:<15}{sale-lost_sale:^20}{item_price_formatted:>10}{sales_total_formatted:>14}"
                
                print(sales_line_item) #displays each item's sale details
            
            sales_total_line_item='$ '+f"{total_sales_amt:.2f}" #formats to to display 2 places after decimal point
            print("-"*total_sales_header_length)
            print(f"TOTAL{sales_total_line_item:>58}") #displays the totals

            #diplays the lost sales report
            print('\n\nLost Sales') #display the lost sales report heading

            lost_sales_header=f"{'#':<4}{'Item':<15}{'Sales':^20}{'Price per Item':^10}{'Total':>10}"
            lost_sales_header_length=len(lost_sales_header)
            print(lost_sales_header) #diplays the lost sales header
            print("="*lost_sales_header_length)

            total_lost_sales_amt=0 #itializes the total lost sales amount as 0
            for i in range(0,self._no_of_items): 
                item_name=self._list_of_dicts_csv[i]['Item'] #gets the item name of the ith item and stores it in a variable
                lost_sale=self._lost_sales[item_name] #stores the lost sales of ith item in a variable
                item_price=float(self._list_of_dicts_csv[i]['Price per Item']) #gets the value corresponding to the key and stores the value in a variable after converting to floating point data type
                item_price_formatted='$ '+f"{item_price:.2f}" #format the item price to display 2 places after decimal point
                lost_sales_total=lost_sale*item_price #calculates the lost sales total of the current item
                total_lost_sales_amt+=lost_sales_total #increments the total lost sales amount with the total lost sales total of the current item
                lost_sales_total_formatted='$ '+f"{lost_sales_total:.2f}" #formats to to display 2 places after decimal point
                sl_no=str(i+1)+'.' #sl no of the report
                lost_sales_line_item=f"{sl_no:<4}{item_name:<15}{lost_sale:^20}{item_price_formatted:>10}{lost_sales_total_formatted:>14}"
            
                print(lost_sales_line_item) #displays each item's lost sale details
            
            lost_sales_total_line_item='$ '+f"{total_lost_sales_amt:.2f}" #formats to to display 2 places after decimal point
            print("-"*lost_sales_header_length)
            print(f"TOTAL{lost_sales_total_line_item:>58}") #displays the totals



            #diplays the Restock report
            print('\n\nRestock') #display the restock report heading

            restock_header=f"{'#':<4}{'Item':<15}{'Demand':^20}{'20%':^20}{'Total Demand':^20}{'Current Stock':^20}{'From Warehouse':>10}"
            restock_header_length=len(restock_header)
            print(restock_header) #diplays the Restock header
            print("="*restock_header_length)

            for i in range(0,self._no_of_items): 
                item_name=self._list_of_dicts_csv[i]['Item'] #gets the item name of the ith item and stores it in a variable
                sale=self._sales[item_name] #stores the sales of ith item in a variable
                sl_no=str(i+1)+'.' #sl no of the report
                demand=sale #assigns the current demand as the total sales made including the lost sales
                demand_20_per=round(0.2*demand) #calculates 20 percent of current demand and rounds off to 2 decimal points and stores the result in a variable
                total_demand=demand+demand_20_per #calculates the total demand by adding up current demand and 20% of current current demand
                current_stock=self._stocks[item_name] #current stock is assigned with value stored in stock
                if current_stock>total_demand: #checks if current stock is more than the total demand
                    from_warehouse=0 #stock to be procured from warehouse is assigned as 0 since current stock is more than the total demand
                else:
                    from_warehouse=total_demand-current_stock #stock to be procured from warehouse is calculated as the difference of total demand and current stock

                self._warehouse[item_name]=from_warehouse #adds key, value pairs to the warehouse dictionary
                restock_line_item=f"{sl_no:<4}{item_name:<15}{demand:^20}{demand_20_per:^20}{total_demand:^20}{current_stock:^20}{from_warehouse:>14}"
                
                print(restock_line_item) #displays each item's restock details        
            
            f.close()
            sys.stdout=sys.__stdout__  

            self._outputVar.set('Reports Generated!')       


    def _export_file(self): 
        clr = os.system('cls')   
        file_name_1=self._file_name.get()
        self._file_name_2=self._export_file_name.get()
        if self._file_name_2=="Enter the csv file name to export":
            self._file_name_2=""
        
        if file_name_1=="Select a file":
            file_name_1=""

        if self._file_name_2=="":
            showerror(message="Error: Please provide an Export CSV filename", parent=self)
        
        elif file_name_1=="":
            showerror(message="Error: Please import the CSV file first before exporting the updated stocks", parent=self)
        else:
            self._list_of_dicts_csv_new=[] #initialises the new list of dictionaries

            for dicts in self._list_of_dicts_csv: #iterates over each dictionary in the list of dictionaries
                item_name=dicts['Item'] #gets the item name from each dictionary and stores the item name in a variable
                dicts['Current Stock']=str(self._stocks[item_name]+self._warehouse[item_name]) #adds the current stock with the the items brought in from the warehouse and stores in a dictionary
                self._list_of_dicts_csv_new.append(dicts) #adds each dictionary to the new list of dictionaries

            self._write_csv(self._list_of_dicts_csv_new,self._file_name_2) #calls the function to write the new stocks details to the csv file
            self._outputVar.set('Export Success!')



def main():
    "Instantiate and pop up the window."
    master=Tk()
    master.iconbitmap('icon.ico')
    StoreStockCalculator().mainloop()

clr = os.system('cls')
main()