from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime
import math
import os
import random


conn=sqlite3.connect(r"C:\Users\Smita Sharma\Desktop\genstore\storems\database\store.db")
c=conn.cursor()


#date
date=datetime.datetime.now().date()

#temporary lists like sessions
product_list=[]
product_price=[]
product_quantity=[]
product_id=[]

#list for labels
labels_list=[]
class Application:
    def __init__(self, master, *args, **kwargs):

        self.master=master
        #frames
        self.left=Frame(master, width=800, height=768, bg='white')
        self.left.pack(side=LEFT)

        self.right=Frame(master, width=566, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        #components
        self.heading=Label(self.left, text='General Store', font=('arial 40 bold'), bg='white')
        self.heading.place(x=0,y=0)

        self.date_l=Label(self.right, text="Today's Date: " + str(date), font=('arial 16 bold'), bg='lightblue', fg='white')
        self.date_l.place(x=0, y=0)

        #table invoice=========================================================================================================
        self.tproduct= Label(self.right, text="Products", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tproduct.place(x=0,y=60)


        self.tquantity= Label(self.right, text="Quantity", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tquantity.place(x=200,y=60)


        self.tamount= Label(self.right, text="Amount", font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tamount.place(x=400,y=60)


        #enter stuff
        self.enterid=Label(self.left, text="Enter Product's ID", font=('arial 18 bold'), bg='white')
        self.enterid.place(x=0,y=80)

        self.enteride= Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enteride.place(x=220, y=80)
        self.enteride.focus()

        #button
        self.search_btn= Button(self.left, text='Search', width=25, height=2, bg='orange', command=self.ajax)
        self.search_btn.place(x=360,y=120)


        #fill it later by the ajax function
        self.productname=Label(self.left, text="", font=('arial 18 bold'), bg='white', fg='steelblue')
        self.productname.place(x=0,y=250)


        self.pprice=Label(self.left, text="", font=('arial 18 bold'), bg='white', fg='steelblue')
        self.pprice.place(x=0,y=290)

        #total label
        self.total_l=Label(self.right, text='', font=('arial 40 bold'), bg='lightblue', fg='white')
        self.total_l.place(x=0,y=600)

        self.master.bind("<Return>", self.ajax)
        self.master.bind("<space>",self.generate_bill)


    def ajax(self, *args, **kwargs):
        self.get_id = self.enteride.get()
        #get the products info with that ID and fill it in the labels above
        query= "SELECT * FROM inventory WHERE id=?"
        result= c.execute(query, (self.get_id, ))
        for self.r in result:
            self.get_id=self.r[0]
            self.get_name=self.r[1]
            self.get_price=self.r[4]
            self.get_stock=self.r[2]
        self.productname.configure(text="Product's Name: " + str(self.get_name))
        self.pprice.configure(text="Price Rs. " + str(self.get_price))

        #create the quantity and the discount label
        self.quantity_l=Label(self.left, text="Enter Quantity", font=('arial 18 bold'), bg='white')
        self.quantity_l.place(x=0,y=370)

        self.quantity_e=Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.quantity_e.place(x=220, y=370)
        self.quantity_e.focus()



        #discount

        self.discount_l=Label(self.left, text="Enter Discount", font=('arial 18 bold'), bg='white')
        self.discount_l.place(x=0,y=410)

        self.discount_e=Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.discount_e.place(x=220, y=410)
        self.discount_e.insert(END, 0)


        #add to cart button
        self.add_to_cart_btn= Button(self.left, text='Add to Cart', width=25, height=2, bg='orange', command=self.add_to_cart)
        self.add_to_cart_btn.place(x=360,y=450)


        #generate bill and change
        self.change_l=Label(self.left, text='Given Amount', font=('arial 18 bold'), bg='white')
        self.change_l.place(x=0, y=550)

        self.change_e=Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.change_e.place(x=220,y=550)


        #button change
        self.change_btn= Button(self.left, text='Calculate Change', width=25, height=2, bg='orange', command=self.change_func)
        self.change_btn.place(x=360,y=590)

        #generate bill button
        self.bill_btn= Button(self.left, text='Generate Bill', width=50, height=2, bg='green', fg='white', command=self.generate_bill)
        self.bill_btn.place(x=155,y=640)


    def add_to_cart(self, *args, **kwargs):
        #get the quantity value and from the database
        self.quantity_value=int(self.quantity_e.get())
        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo("Error", "Not that much products in inventory")
        else:
            #calculate the price
            self.final_price= (float(self.quantity_value) * float(self.get_price))-(float(self.discount_e.get()))
            product_list.append(self.get_name)
            product_price.append(self.final_price)
            product_quantity.append(self.quantity_value)
            product_id.append(self.get_id)

            self.x_index=0
            self.y_index=100
            self.counter=0
            for self.p in product_list:
                self.tempname= Label(self.right, text=str(product_list[self.counter]), font=('arial 18 bold'), bg='lightblue',fg='white')
                self.tempname.place(x=0, y=self.y_index)
                labels_list.append(self.tempname)


                self.tempqt= Label(self.right, text=str(product_quantity[self.counter]), font=('arial 18 bold'), bg='lightblue',fg='white')
                self.tempqt.place(x=200, y=self.y_index)
                labels_list.append(self.tempqt)


                self.tempprice= Label(self.right, text=str(product_price[self.counter]), font=('arial 18 bold'), bg='lightblue',fg='white')
                self.tempprice.place(x=400, y=self.y_index)
                labels_list.append(self.tempprice)

                self.y_index+=40
                self.counter+=1

                #total configure
                self.total_l.configure(text='Total: Rs. ' + str(sum(product_price)))

                #delete
                self.quantity_l.place_forget()
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.productname.configure(text='')
                self.pprice.configure(text='')
                self.add_to_cart_btn.destroy()


                #autofocus to the enter id
                self.enteride.focus()
                self.enteride.delete(0, END)



    def change_func(self, *args, **kwargs):
        #get the amount given by the customer and the amount generated by the computer
        self.amount_given=float(self.change_e.get())
        self.our_total=float(sum(product_price))
        self.to_give = self.amount_given - self.our_total

        #label change
        self.c_amount= Label(self.left, text='Change is: Rs. ' + str(self.to_give), font=('arial 18 bold'), fg='red',bg='white')
        self.c_amount.place(x=0, y=600)



    def generate_bill(self, *args, **kwargs):
        #create the bill before updating the databse
        directory="C:/Users/Smita Sharma/Desktop/genstore/storems/invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        #templates for the bill
        company="\t\t\t\t MAMTA TRADING \n"
        address="\t\t\t\t Boro Chowk, Zoo Narengi Road \n"
        address2="\t\t\t\t Mathgharia-2, Guwahati,Assam-781026 \n"
        phone="\t\t\t\t 6002797488(WORK) \n"
        phone2="\t\t\t\t 9127211593(HOME) \n"
        sample="\t\t\t\tINVOICE\n"
        dt="\t\t\t\t" + str(date)

        table_header="\n\n\t\t\t............................................................................\n\t\t\tSN.\tProducts\t\tQty\tAmount\n\t\t\t............................................................................"
        final=company + address + address2 + phone + phone2 + sample + dt + "\n" + table_header
        #open a file and write to it
        file_name=str(directory) + str(random.randrange(5000,10000)) + ".txt"
        f= open(file_name, 'w')
        f.write(final)

        #fill dynamics
        r=1
        i=0
        for t in product_list:
            f.write("\n\t\t\t" + str(i) + "\t" + str(product_list[i] + "......."[:7]) + "\t\t" + str(product_quantity[i]) + "\t" + str(product_price[i]))
            i+=1
            r+=1
        f.write("\n\n\t\t\t\t\t\tTotal Rs. " + str(sum(product_price)))
        f.write("\n\t\t\t\tThanks for Visiting")
        os.startfile(file_name,"print")
        f.close()
        
                
        #decrease the stock
        self.x=0

        initial= "SELECT * FROM inventory WHERE id=?"
        result=c.execute(initial,(product_id[self.x], ))
        
        for i in product_list:
            for r in result:
                self.old_stock=r[2]
            self.new_stock = int(self.old_stock) - int(product_quantity[self.x])

            #updating the stock
            sql= "UPDATE inventory SET stock=? WHERE id=?"
            c.execute(sql, (self.new_stock, product_id[self.x]))
            conn.commit()
            #inserting in the transactions
            sql2="INSERT INTO transactions (product_name, quantity, amount,date) Values (?,?,?,?)"
            c.execute(sql2,(product_list[self.x], product_quantity[self.x], product_price[self.x], date))
            conn.commit()
            self.x+=1
        for a in labels_list:
            a.destroy()

        del(product_list[:])
        del(product_id[:])
        del(product_quantity[:])
        del(product_price[:])
        self.total_l.configure(text="")
        self.c_amount.configure(text="")
        self.change_e.delete(0,END)
        self.enteride.focus()

        tkinter.messagebox.showinfo("Success", "Next Customer, Please")
root=Tk()
b=Application(root)

root.geometry("1366x768+0+0")
root.mainloop()