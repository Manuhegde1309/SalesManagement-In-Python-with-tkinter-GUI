from sys import exit
import mysql.connector as sql
from  tkinter import *
from  tkinter import ttk
from tkinter import messagebox as mb
from datetime import *
Root=Tk()
Root.title("Point of Sale")

Root.geometry("1200x700")
Root.resizable(FALSE,FALSE)

cartItemSQL=[]
gst=0
itemcost=0
orderId=0
 #connecting to database
def connectDB():
    global mydb
    global conn
    user=username.get()
    pas=passwd.get()
    
    conn=sql.connect(host='localhost',user=user,passwd=pas, database='marketing_system_and_sales_system')
    mydb=conn.cursor()
    if conn.is_connected()==True:
        initialiseMenu()
        loginFrame.destroy()
  #removing the frames  
def clearWidget():
    try:
        orderFrame.destroy()
    except:
        print("OrderFrame not created")
    try:    
        cartFrame.destroy()
    except:
        print("CartFrame not created")
    try:
        purchaseFrame.destroy()
    except:
        print("PurchaseFrame not created")
    try:
        findOrderFrame.destroy()
    except:
        print("findOrderFrame not created")
    try:
        PRODUCTFRAME.destroy()
    except:
        print("productFrame not created")
    try:
        productFrame.destroy()
    except:
        print("productFrame not created")
    try:
        addFrame.destroy()
    except:
        print("addframe not defined")

 #loginpage   
def loginWidget():
    
    global username
    global passwd
    username=StringVar()
    passwd=StringVar()
    global loginFrame
    Root.geometry("1110x700")
    loginFrame=LabelFrame(Root, text='Please login to proceed...', fg='blue',bg='violet', pady=10, padx=10,width=100,relief='raised')
    Lbl1=Label(loginFrame,text='User Name:',font=24).grid(row=2,column=0,pady=10)
    Lbl1=Label(loginFrame,text='Password:',font=24).grid(row=3,column=0,pady=10)
    e1=Entry(loginFrame,width=25,textvariable=username,font='arial').grid(row=2,column=1,pady=10)
    e1=Entry(loginFrame,width=25,show='*',textvariable=passwd,font='arial').grid(row=3,column=1,pady=10)

    B=Button(loginFrame,text='Login',command=connectDB, fg='blue', bg='grey',width=10).grid(row=4,column=1, sticky=SE, pady=10)
    loginFrame.grid(padx=400,pady=200)

def logoff():
    emptyMenu=Menu(Root)
    Root.config(menu=emptyMenu)
    clearWidget()
    loginWidget()

#adding more products to database
def ADD():
    if ProductNameVar.get()=="":
        mb.showerror(title='Error',message='Please enter product name')
    else:
        cursor=conn.cursor()
        query="SELECT ProductId, ProductName, UnitPrice, GST_rate,AvailableQty FROM products ORDER BY ProductName"
        cursor.execute(query)
        productList=cursor.fetchall()
        if len(productList)==0:
            Query3='insert into products(ProductName,GST_rate,AvailableQty,UnitPrice) values ('+"'"+ProductNameVar.get()+"'"+','+str(GSTVar.get())+','+str(QtyVar.get())+","+str(costVar.get())+')'
            cursor.execute(Query3)
            conn.commit()
            lbl=Label(addFrame,text='addition successfull').grid(row=10,column=7)
        for row in productList:
            if ProductNameVar.get()!=row[1]:
                Query3='insert into products(ProductName,GST_rate,AvailableQty,UnitPrice) values ('+"'"+ProductNameVar.get()+"'"+','+str(GSTVar.get())+','+str(QtyVar.get())+","+str(costVar.get())+')'
                cursor.execute(Query3)
                conn.commit()
                lbl=Label(addFrame,text='addition successfull').grid(row=10,column=7)
            else:
                mb.showerror(title='Error',message='duplicate entry,please try again')

    
def AddNewProduct():
    clearWidget()
    global addFrame
    global ProductNameVar
    global QtyVar
    global GSTVar
    global costVar
    ProductNameVar=StringVar()
    QtyVar=IntVar()
    GSTVar=IntVar()
    costVar=IntVar()
    addFrame=LabelFrame(text='add new products',font=6,fg='blue',bg='grey')
    Lbl1=Label(addFrame,text='Product Name:',font=24).grid(row=1,column=0,pady=10)
    Lbl2=Label(addFrame,text='Quantity:',font=24).grid(row=2,column=0,pady=10)
    e1=Entry(addFrame,width=25,textvariable=ProductNameVar,font='arial').grid(row=1,column=1,pady=10)
    e2=Entry(addFrame,width=25,textvariable=QtyVar,font='arial').grid(row=2,column=1,pady=10)
    Lbl3=Label(addFrame,text='GST %',font=24).grid(row=3,column=0,pady=10)
    Lbl4=Label(addFrame,text='Price',font=24).grid(row=4,column=0,pady=10)
    e3=Entry(addFrame,width=25,textvariable=GSTVar,font='arial').grid(row=3,column=1,pady=10)
    e4=Entry(addFrame,width=25,textvariable=costVar,font='arial').grid(row=4,column=1,pady=10)
    b=Button(addFrame,text='add to database',command=ADD,width=15,bg='blue',fg='yellow').grid(row=5,column=5)
    addFrame.grid(sticky=NSEW)

#To purchase items 
def addToCart():
    global gst
    global itemcost
    global quantity
    global unitPrice
    global row
    Cursor=conn.cursor()
    for row in productList:
        if(productVar.get() == row[1]):
            unitPrice=row[2]
            quantity = float(quantityVar.get())
            
            if quantity > 0.0 and quantity < row[4]:
                Gst=unitPrice * row[3] / 100
                Itemcost=unitPrice * int(quantityVar.get())
                
                gst=(gst+unitPrice * row[3] / 100)
                itemcost=(itemcost+Gst+Itemcost)
                amount=int(row[4])
                
                query4='UPDATE products SET AvailableQty='+"'"+str(amount-int(quantityVar.get())) + "'" + ' where ProductName=' + '"' + productVar.get() + '"' 

                Cursor.execute(query4)
                conn.commit()
                
                cartItems.insert(parent='',index='0', values=(row[1],str(quantityVar.get()),str(row[2]),format(Gst,'.2f'), format(Itemcost,'.3f')))
                itemSQL = 'INSERT INTO Order_Details (OrderId,ProductId,Quantity,UnitPrice,GST) VALUES (NewID,'+str(row[0])+','+str(quantity)+','+str(unitPrice)+','+str(Gst)+')'
                cartItemSQL.append(itemSQL)
                
                Lbl3=Label(cartFrame,text=gst).grid(row=9,column=2,sticky=E)
                Lbl4=Label(cartFrame,text=itemcost).grid(row=10,column=2,sticky=E)
                
            else:
                mb.showerror(title='Error',message='Please enter valid quantity')

#processing order
def checkout():
    if cartItems.get_children()==tuple():
        mb.showerror(title='Error',message='Please enter the items you wish to purchase')
    else:
        customerId=0
        cursor=conn.cursor()
        customerSQL = 'Select customerId from customer where name="'+ customerName.get() +'"'
        cursor.execute(customerSQL)
        result=cursor.fetchall()
    
        if(len(result)==0):
            customerSQL='insert into customer (Name,PhoneNumber) values ("' + customerName.get() + '","'+ PhoneNumber.get() + '")'
            cursor.execute(customerSQL)
            customerId=cursor.lastrowid        
        else:
            customerId=result[0][0]
        
        query='insert into customer_orders(CustomerId,OrderDate) values('+ str(customerId) + ', "' + str(datetime.now()) + '")'
        cursor.execute(query)
    
        orderId=cursor.lastrowid
        cursor.reset()
        for orderItem in cartItemSQL:
            query=orderItem.replace('NewID',str(orderId))
            cursor.execute(query)
                
            conn.commit()
    
    Bt1=Label(cartFrame,text='purchase successfull',font='Arial').grid(sticky=W)
#acquiring customer details
def CreateOrderWidget():
    clearWidget()
    Root.geometry("1200x700")
    cartItemSQL=[]
    global purchaseFrame
    global orderFrame
    global customerName
    global PhoneNumber
    
    orderFrame=LabelFrame(Root,text='Customer Details', fg='blue', pady=10,bg='grey')
    customerName=StringVar()
    PhoneNumber=StringVar()
    Lbl1=Label(orderFrame,text='Customer Name:').grid(row=1,column=0)
    Lbl2=Label(orderFrame,text='Phone number:  ').grid(row=2,column=0)
    e1=Entry(orderFrame,width=40,textvariable=customerName,font='arial').grid(row=1,column=1)
    e2=Entry(orderFrame,width=40,textvariable=PhoneNumber,font='arial').grid(row=2,column=1)
    
    global productList
    cursor=conn.cursor()
    query="SELECT ProductId, ProductName, UnitPrice, GST_rate,AvailableQty FROM products ORDER BY ProductName"
    cursor.execute(query)
    productList=cursor.fetchall()
    purchaseFrame=LabelFrame(Root,text='Select the items to purchase',fg='blue',bg='grey',width=100)

     #Order line
    global productVar
    global quantityVar
    productVar=StringVar()
    quantityVar=DoubleVar()
    Lbl3=Label(purchaseFrame,text='   Select Product').grid(row=3,column=0,sticky=E,pady=10)
    productCombo=ttk.Combobox(purchaseFrame,textvariable=productVar,values=[row[1] for row in productList])
    productCombo.current(0)
    productCombo.grid(row=3, column=1)

    Lbl3=Label(purchaseFrame,text='Quantity   ',width=12).grid(row=4,column=0)
    entry=Entry(purchaseFrame,textvariable=quantityVar,width=22).grid(row=4,column=1)

    button=Button(purchaseFrame, text="Add To Cart",command=addToCart,width=10,bg='blue',fg='yellow').grid(row=5,column=8)

    global cartFrame
    cartFrame=LabelFrame(text='List of items in cart',fg='blue',bg='grey',width=100)
    columns=('item','quantity','unitPrice','gst','total')
    global cartItems
    
    cartItems=ttk.Treeview(cartFrame,columns=columns,show='headings')
    cartItems.heading('item',text='Item Name',anchor='w')
    cartItems.heading('quantity',text='Quantity',anchor='w')
    cartItems.heading('unitPrice',text='Unit Price',anchor='w')
    cartItems.heading('gst',text='GST',anchor='w')
    cartItems.heading('total',text='Total Amount',anchor='w')
    cartItems.grid(row=7,column=0,sticky=NSEW)
    
    Lbl1=Label(cartFrame,text='Total GST:').grid(row=9,column=1,sticky=E)
    Lbl2=Label(cartFrame,text='Grand total:').grid(row=10,column=1,sticky=E)
    
    button=Button(cartFrame, text='Checkout',command=checkout,width=10,bg='blue',fg='yellow')
    button.grid(row=11, column=1, sticky=E)

    orderFrame.grid(row=1,column=0,sticky=W,pady=10,ipady=20)
    purchaseFrame.grid(column=0,sticky=W,pady=10,ipady=20)
    cartFrame.grid(column=0,pady=10,ipady=20)

#list of all available products
def ListAllProducts():
    clearWidget()
    global PRODUCTFRAME

    Cursor=conn.cursor()
    PRODUCTFRAME=LabelFrame(text='List of all products',font=6,fg='blue',bg='grey')
    columns=('item','quantity','unitPrice','gst')
    ProdItems=ttk.Treeview(PRODUCTFRAME,columns=columns,show='headings')
    ProdItems.heading('item',text='Item Name',anchor='w')
    ProdItems.heading('quantity',text='Quantity',anchor='w')
    ProdItems.heading('unitPrice',text='Unit Price',anchor='w')
    ProdItems.heading('gst',text='GST',anchor='w')
    
    query5='select * from products'
    Cursor.execute(query5)
    
    products=Cursor.fetchall()

    for row in products:
        ProdItems.insert(parent='',index='0',values=(row[1],row[3],row[4],row[2]))
    ProdItems.grid(row=7,column=0)

    PRODUCTFRAME.grid(rowspan=600,columnspan=1000)

#record of previous orders
def OnSaleItemChange(r):
    curItem = saleItems.focus()
    selectedOrderline=saleItems.item(curItem)
    connectDB()
    cursor=conn.cursor()

    curItem = saleItems.focus()
    selectedOrderline=saleItems.item(curItem)
    query2='select OrderId, ProductId, Quantity, UnitPrice, GST from order_details where OrderId=' + str(selectedOrderline['values'][0]) 
    
    cursor.execute(query2)
    productList=cursor.fetchall()
    for i in saleItems2.get_children():
        saleItems2.delete(i)

    for row in productList:
        saleItems2.insert(parent='',index='0', values=(row[1],row[2],row[3],row[4]))
    
def findSale():
    clearWidget()
    Root.geometry('1200x600')
    connectDB()
    global saleItems
    global saleItems2
    global productFrame
    global findOrderFrame
    findOrderFrame=LabelFrame(text='list of customers',fg='blue',bg='grey')
    columns1=('OrderId','Name','Ordertime')
    cursor=conn.cursor()
    saleItems=ttk.Treeview(findOrderFrame,columns=columns1,show='headings',)
    saleItems.heading('OrderId',text='Invoice No',anchor='w')
    saleItems.heading('Name',text='Name',anchor='w')
    saleItems.heading('Ordertime',text='Time of purchase',anchor='w')
    query='select OrderId, Name, OrderDate from customer, customer_orders  where customer.CustomerId=customer_orders.CustomerId'
    cursor.execute(query)
    sale=cursor.fetchall()
    
    for i in range(len(sale)):
        saleItems.insert(parent='',index='0', values=(sale[i][0], sale[i][1], sale[i][2]))
    
    saleItems.bind('<<TreeviewSelect>>', OnSaleItemChange)
    saleItems.grid(row=1,column=1,sticky=NSEW)

    productFrame=LabelFrame(text='Order Details',fg='blue',bg='grey')
    column2=('ProductId','Quantity','UnitPrice','GST')
    saleItems2=ttk.Treeview(productFrame,columns=column2,show='headings')
    saleItems2.heading('ProductId',text='Id',anchor='w')
    saleItems2.heading('Quantity',text='Quantity',anchor='w')
    saleItems2.heading('UnitPrice',text='UnitPrice',anchor='w')
    saleItems2.heading('GST',text='GST',anchor='w')
    findOrderFrame.grid(pady=10,sticky=W)
    saleItems2.grid(row=1,column=1,sticky=NSEW)
    productFrame.grid(pady=10)


#creating the menu bar
def initialiseMenu():
    my_menu=Menu(Root)
    Root.config(menu=my_menu)
    product_menu = Menu(my_menu,tearoff=0)
    my_menu.add_cascade(label="Products",menu=product_menu)
    product_menu.add_command(label="List Products",command=ListAllProducts)
    product_menu.add_command(label="New Product",command=AddNewProduct)

    sales_menu = Menu(my_menu,tearoff=0)
    my_menu.add_cascade(label="Sales",menu=sales_menu)
    sales_menu.add_command(label="New Sale", command=CreateOrderWidget)
    sales_menu.add_command(label="Find Sale",command=findSale)

    logoff_menu = Menu(my_menu,tearoff=0)
    my_menu.add_cascade(label="Logout",menu=logoff_menu)
    logoff_menu.add_command(label="Logoff",command=logoff)

loginWidget()
Root.configure(bg='cyan')

Root.mainloop()