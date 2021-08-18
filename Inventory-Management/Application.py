from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk
from hexAndString import *
from DES import *
import mysql.connector as SQL
import datetime

file_location="Licence.txt"
root = Tk()
root.geometry("1920x1080")
root.title("Login Page")
folder_location = "F:\\softwareproject\\"

db_host = "" #127.0.0.1
db_port = "" #3306
db_user = "" #root
db_database = "" #IMS
db_password = "" #Mdif59x02#
# Set Password = G@Aadhithyaa@2002

def infoExtraction(key):
    
    # Converting The Password guard enters to 64-bit DES-key
    key=string2hex(key)

    # Opening the encrypted file stored in memory and copying first 16 char to msg
    a=open(folder_location + file_location)
    text=a.read()
    a.close()
    msg=text.split("\n")

    # Decrypting the msg using key(in a cyclic way)
    len_msg=len(msg)
    len_key=len(key)-1
    password=[]
    for i in range(len_msg):
        password.append(DESAlgorithm(key[i%len_key],msg[i],ch=2))

    # Converting The Password from 64-bit DES-Decryption to String
    password=hex2string(password)
    global db_host, db_port, db_user, db_database, db_password
    
    try:
        db_host, db_port, db_user, db_database, db_password = password.split("\n")
    except:
        pass
    return None

def Login():
    try:
        global cursor, con
        con = SQL.connect(host=db_host, user=db_user, password=db_password, database=db_database, port = int(db_port), auth_plugin='mysql_native_password', autocommit=False)
        cursor=con.cursor()
        return True
    except SQL.errors.ProgrammingError:
        return False

def login_page():
    def login():
        infoExtraction(loginvar.get())
        if Login()==True:
            topframe.place_forget()
            mainframe.place_forget()
            loginframe.place_forget()
            start()
        return None

    topframe = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
    topframe.place(x=0, y=0)
    title = Label(topframe, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue", anchor='center')
    title.config(font="Georgia 30 bold")
    title.place(x=300, y=30)
    mainframe = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
    mainframe.place(x=350, y=140)
    welcome = Label(mainframe, text='Welcome! Please Log In to Proceed', fg='white', bg='sky blue', anchor='center')
    welcome.config(font="Georgia 20 bold")
    welcome.place(x=130, y=20)
    loginframe = Frame(root, width=720, height=200, bg="sky blue")
    loginframe.place(x=530, y=260)
    loginvar = StringVar(value="Password")
    loginentry = Entry(loginframe, textvariable=loginvar, font="georgia 15", width=25, bg="white")
    loginentry.config(show='*')
    loginentry.place(x=50, y=0, height=40)
    loginbtn = Button(loginframe, text="  Log In  ", font="Georgia 11 bold", bg="white", bd=5, command=login)
    loginbtn.place(x=150, y=70, height=40)

    root.config(bg='sky blue')
    root.mainloop()
    return None

def start():

    root.title("Home Page")

    def put_in_table(tree_obj, data):
        for i in tree_obj.get_children():
            tree_obj.delete(i)
        for i in range(len(data)):
            tree_obj.insert(parent="", index=i, iid=i, values=data[i])
        return None

    def inventory_page():
        topframe.place_forget()
        mainframe.place_forget()
        buttonframe.place_forget()
        root.title("Inventory Page")

        def back():
            tableframe.place_forget()
            formframe.place_forget()
            topframe1.place_forget()
            mainframe1.place_forget()
            searchframe.place_forget()
            start()
            return None

        def searchprod():
            query = "SELECT * FROM Stock "
            if (searchvar.get() != "" and searchvar.get() != "ItemID or ItemName"):
                query += "WHERE ItemID LIKE '%" + searchvar.get() + "%' OR ItemName LIKE '%" + searchvar.get() + "%';"
            cursor.execute(query)
            reply = cursor.fetchall()
            put_in_table(tree, reply)
            return None

        def add_new_stock():
            # print(itemid.get(), itemname.get(), costprice.get(), quantity.get(), supplierinfo.get())
            query = "INSERT INTO stock VALUES (\""
            
            if itemid.get() == "":
                cursor.execute("SELECT COUNT(*) FROM stock;")
                itemid.set(str(int(cursor.fetchall()[0][0]) + 1))
            query += itemid.get() + "\""
            
            if itemname.get() == "" or itemname.get() == "Mandatory Input":
                itemname.set("Mandatory Input")
                return None
            else:
                query += ", \"" + itemname.get() + "\""
            
            if costprice.get() == "":
                costprice.set("Mandatory Input")
                return None
            else:
                try:
                    int(costprice.get())
                except:
                    costprice.set("Only a Number")
                    return None
                query += ", " + costprice.get()
            
            if quantity.get() == "":
                quantity.set("0")
            else:
                try:
                    int(quantity.get())
                except:
                    quantity.set("Only a Number")
                    return None
            query += ", " + quantity.get()
            
            if supplierinfo.get() == "" and supplierinfo.get() == "Mandatory Input":
                supplierinfo.set("Mandatory Input")
                return None
            else:
                query += ", \"" + supplierinfo.get() + "\");"
            cursor.execute(query)
            searchprod()
            return None
        
        def delproduct():
            if (itemid.get() == "" or itemid.get() == "Mandatory Entry"):
                itemid.set("Mandatory Entry")
            else:
                query = "DELETE FROM stock WHERE ItemID = \"" + itemid.get() + "\";"
                # print(query)
                cursor.execute(query)
                searchprod()
            return None

        def update_product():
            query = "UPDATE stock SET "
            if (itemid.get() == "" or itemid.get() == "Mandatory Entry"):
                itemid.set("Mandatory Entry")
                return None
            
            if itemname.get() != "":
                query += "ItemName = \"" + itemname.get() + "\", "
            
            if costprice.get() != "":
                query += "CostPrice = " + costprice.get() + ", "
            
            if quantity.get() != "":
                query += "Qty = " + quantity.get() + ", "

            if supplierinfo.get() != "":
                query += "SupNo = " + supplierinfo.get() + ", "
            
            if (itemname.get()!="" or costprice.get()!="" or quantity.get()!="" or supplierinfo.get()!=""):
                query = query[:-2] + " WHERE ItemID = \"" + itemid.get() + "\";"
                print(query)
                cursor.execute(query)
                searchprod()
            return None

        def select_record():
            itm = tree.focus()
            if itm == "":
                return None
            else:
                itm = tree.item(itm, "values")
                itemid.set(itm[0])
                itemname.set(itm[1])
                costprice.set(itm[2])
                quantity.set(itm[3])
                supplierinfo.set(itm[4])
            return None

        
        topframe1 = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
        topframe1.place(x=0, y=0)
        title = Label(topframe1, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue",anchor='center')
        title.config(font="Georgia 30 bold")
        title.place(x=320, y=30)

        mainframe1 = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
        mainframe1.place(x=350, y=100)
        welcome = Label(mainframe1, text='Welcome to Inventory Page', fg='white', bg='sky blue', anchor='center')
        welcome.config(font="Georgia 20 bold")
        welcome.place(x=200, y=30)
        
        formframe = Frame(root, width=500, height=450, bg="#FFFFFF")
        formframe.place(x=100, y=315)
        tableframe = LabelFrame(root, width=1300, height=400)
        tableframe.place(x=700, y=315)

        searchframe = Frame(root, width=720, height=70, bg="sky blue")
        searchframe.place(x=400, y=200)
        im = PhotoImage(file = folder_location + "images\\searchdesc.png", master=root)
        im = im.subsample(8, 8)
        backbtn = Button(searchframe, text="Back", font="Georgia 11 bold", bg="white", command=back)
        backbtn.place(x=0, y=20)
        searchbtn = Button(searchframe, text="  Search Item  ", font="Georgia 11 bold", bg="white", bd=5, image=im,compound=LEFT, command=searchprod)
        searchbtn.place(x=450, y=20, height=40)
        searchvar = StringVar(value="ItemID or ItemName")
        searchentry = Entry(searchframe, textvariable=searchvar, font="georgia 15", width=25, bg="white")
        searchentry.place(x=130, y=20, height=40)

        scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(tableframe, orient=VERTICAL)
        tree = ttk.Treeview(tableframe,columns=("Item ID", "Item Name", "Cost Price", "Quantity", "Supplier Number"),selectmode="browse", height=18, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        column_width = {"#0": 0, "#1": 100, "#2": 100, "#3": 150, "#4": 150, "#5": 150}
        column_heading = ['Item ID', 'Item Name', 'Cost Price', 'Quantity', 'Supplier Number']
        for i in column_width:
            tree.column(i, stretch=YES, minwidth=0, width=column_width[i])
        for i in column_heading:
            tree.heading(i, text=i, anchor=CENTER)
        tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        formframe.focus_set()
        itemid = StringVar()
        itemname = StringVar()
        costprice = StringVar()
        quantity = StringVar()
        supplierinfo = StringVar()
        va = 20
        for i in range(5):
            Label(formframe, text=column_heading[i], font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(formframe, textvariable=itemid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=20,height=30)
        Entry(formframe, textvariable=itemname, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=80,height=30)
        Entry(formframe, textvariable=costprice, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=140,height=30)
        Entry(formframe, textvariable=quantity, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=200,height=30)
        Entry(formframe, textvariable=supplierinfo, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=260,height=30)
        Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_new_stock).place(x=10, y=361)
        Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_product).place(x=130, y=361)
        Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=delproduct).place(x=250, y=361)
        Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_record).place(x=370, y=361)
        

        root.config(bg="sky blue")
        root.mainloop()

        return None

    def sales():
        topframe.place_forget()
        mainframe.place_forget()
        buttonframe.place_forget()
        root.title("Sales Page")

        def back():
            topframe3.place_forget()
            mainframe3.place_forget()
            formframe.place_forget()
            tableframe1.place_forget()
            searchframe.place_forget()
            start()

        def search_order():
            query = "SELECT * FROM orders "
            if searchvar.get() != "":
                query += "WHERE OrderID LIKE \"%{}%\" OR Platform LIKE \"%{}%\";".format(searchvar.get(), searchvar.get().capitalize())
            # print(query)
            cursor.execute(query)
            data = cursor.fetchall()
            put_in_table(tree, data)
            last_search = search_order
            return None
        
        def search_using_form_data():
            # print(orderid.get(), platform.get(), orderdate.get(),"if check: ",include_checkbox_chk.get(), processed_chk.get(), packed_chk.get(), sent_chk.get(), returned_chk.get(), money_recieved_chk.get(), returndate.get())
            query = "SELECT * from orders "

            def check_where(Query):
                if "WHERE" != Query[21:26]:
                    Query += "WHERE "
                return Query

            if orderid.get() != "" and orderid.get() != "Mandatory Entry":
                query += "WHERE OrderID LIKE \"%{}%\" AND ".format(orderid.get())

            if platform.get() != "" and platform.get() != "Mandatory Entry":
                query = check_where(query)
                query += "Platform LIKE \"%{}%\" AND ".format(platform.get().capitalize())
            
            if include_checkbox_chk.get() == 1:
                query = check_where(query)
                query += "Processed = {} AND Packed = {} AND Sent = {} AND Returned = {} AND MoneyRecieved = {} AND "
                query = query.format(processed_chk.get(), packed_chk.get(), sent_chk.get(), returned_chk.get(), money_recieved_chk.get())

            if orderdate.get() != "" and orderdate.get() != "YYYY-MM-DD":
                query = check_where(query)
                query += "OrderDate LIKE \"%{}%\" AND ".format(orderdate.get())

            if returned_chk.get() == 1 and include_checkbox_chk.get() == 1:
                if returndate.get() != "" and returndate.get() != "YYYY-MM-DD":
                    query = check_where(query)
                    query += "ReturnedDate LIKE \"%{}%\" AND ".format(returndate.get())
            
            if query[-4:] == "AND ":
                query = query[0:-4]
            # print(query)
            cursor.execute(query)
            data = cursor.fetchall()
            put_in_table(tree, data)
            last_search = search_using_form_data
            return None
        
        last_search = search_order

        def add_new_order():
            # print(orderid.get(), platform.get(), orderdate.get(), processed_chk.get(), packed_chk.get(), sent_chk.get(), returned_chk.get(), money_recieved_chk.get(), returndate.get())
            query = "INSERT INTO orders VALUES ("
            if orderid.get() == "" or orderid.get() == "Mandatory Entry":
                orderid.set("Mandatory Entry")
                return None
            query += "\"" + orderid.get() + "\", "

            if platform.get() == "" or platform.get() == "Mandatory Entry":
                platform.set("Mandatory Entry")
                return None
            query += "\"" + platform.get().capitalize() + "\", "

            query += str(processed_chk.get()) + ", "
            query += str(packed_chk.get()) + ", "
            query += str(sent_chk.get()) + ", "
            query += str(returned_chk.get()) + ", "
            query += str(money_recieved_chk.get()) + ", "
            query += "0, " # TotalAmount

            if orderdate.get() == "" or orderdate.get() == "YYYY-MM-DD":
                orderdate.set(datetime.datetime.today().strftime('%Y-%m-%d'))
            query += "\"" + orderdate.get() + "\", "

            if returned_chk.get() == 1:
                if returndate.get() == "" or returndate.get() == "YYYY-MM-DD":
                    returndate.set(datetime.datetime.today().strftime('%Y-%m-%d'))
                query += "\"" + returndate.get() + "\", "
            else:
                query += "NULL" + ");"
            
            # print(query)
            cursor.execute(query)
            last_search()
            return None

        def update_order():
            query = "UPDATE orders SET "
            if orderid.get() in ["", "Mandatory Entry"]:
                orderid.set("Mandatory Entry")
                return None
            
            if platform.get() not in ["", "Mandatory Entry"]:
                query += "Platform = \"{}\", ".format(platform.get().capitalize())

            if orderdate.get() not in ["", "YYYY-MM-DD"]:
                query += "OrderDate = \"{}\", ".format(orderdate.get())

            query += "Processed = {}, Packed = {}, Sent = {}, Returned = {}, MoneyRecieved = {}, "
            query = query.format(processed_chk.get(), packed_chk.get(), sent_chk.get(), returned_chk.get(), money_recieved_chk.get())

            if returned_chk.get() == 1:
                if returndate.get() in ["", "YYYY-MM-DD", "None"]:
                    returndate.set("Mandatory Entry")
                    return None
                else:
                    query += "ReturnedDate = \"{}\", ".format(returndate.get())
            
            query = query[:-2] + " WHERE OrderID = \"{}\";".format(orderid.get())
            # print(query)
            cursor.execute(query)
            last_search()
            return None

        def remove_order():
            query = "DELETE FROM orders WHERE OrderID = \""
            if orderid.get() in ["", "Mandatory Entry"]:
                orderid.set("Mandatory Entry")
                return None
            query += orderid.get() + "\";"
            cursor.execute(query)
            last_search()
            return None

        def double_click(event = None):
            
            def search_orderid():
                order_id.set(order_id.get())
                if order_id.get() in ["", "Mandatory Entry"]:
                    order_id.set("Mandatory Entry")
                    return None
                query = "SELECT ProductID, Qty, Amount FROM order_details WHERE OrderID = \"{}\";".format(order_id.get())
                cursor.execute(query)
                data = cursor.fetchall()
                put_in_table(tree2, data)
                return None
            
            def back():
                root1.destroy()
                return None
            
            def add_order_detail():
                # orderid.get(), productid.get(), quantity.get()
                if order_id.get() in ["", "Mandatory Entry"]:
                    order_id.set("Mandatory Entry")
                    return None
                
                if productid.get() in ["", "Mandatory Entry"]:
                    productid.set("Mandatory Entry")
                    return None
                
                if quantity.get() in ["", "Mandatory Entry"]:
                    quantity.set("Mandatory Entry")
                    return None
                try:
                    int(quantity.get())
                except:
                    quantity.set("Only Number")
                    return None
                query = "INSERT INTO order_details (OrderID, ProductID, Qty) VALUES (\"{}\", \"{}\", {});"
                query = query.format(order_id.get(), productid.get(), quantity.get())
                cursor.execute(query)
                search_orderid()
                return None
            
            def delete_product_from_detail():
                if order_id.get() in ["", "Mandatory Entry"]:
                    order_id.set("Mandatory Entry")
                    return None
                
                if productid.get() in ["", "Mandatory Entry"]:
                    productid.set("Mandatory Entry")
                    return None

                query = "DELETE FROM order_details WHERE OrderID = \"{}\" AND ProductID = \"{}\";"
                query = query.format(order_id.get(), productid.get())
                cursor.execute(query)
                return None
            
            def select_record():
                if tree2.focus() != "":
                    itm = tree2.focus()
                    itm = tree2.item(itm, 'values')
                    productid.set(itm[0])
                    quantity.set(itm[1])
                return None
            
            root1 = Toplevel()
            root1.geometry("1050x500+200+200")
            root1.title("Orders Window")

            formframe = Frame(root1, width=500, height=350, bg="#FFFFFF")
            formframe.place(x=20, y=80)

            tableframe = LabelFrame(root1, width=600, height=400)
            tableframe.place(x=550, y=40)

            im = PhotoImage(file = folder_location + "images\\searchdesc.png", master=root1)
            im = im.subsample(8, 8)
            searchbtn = Button(formframe, text="  Search Order  ", font="Georgia 11 bold", bg="white", bd=5, image=im,compound=LEFT, command=search_orderid)
            searchbtn.place(x=330, y=15, height=35)
            scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
            scrollbary = Scrollbar(tableframe, orient=VERTICAL)
            tree2 = ttk.Treeview(tableframe,columns=("Product ID", "Quantity","Amount"),selectmode="browse", height=18, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
            column_width = {"#0": 0, "#1": 150, "#2": 150, "#3": 150}
            column_heading=["Product ID", "Quantity","Amount"]
            for i in column_width:
                tree2.column(i, stretch=YES, minwidth=0, width=column_width[i])
            for i in column_heading:
                tree2.heading(i, text=i, anchor=CENTER)
            tree2.grid(row=1, column=0, sticky="W")
            scrollbary.config(command=tree2.yview)
            scrollbarx.grid(row=2, column=0, sticky="we")
            scrollbarx.config(command=tree2.xview)
            scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
            formframe.focus_set()

            order_id = StringVar()
            if tree.focus() != "":
                itm = tree.item(tree.focus(), "values")
                print(itm)
                itm = itm[0]
                order_id.set(itm)
            productid = StringVar()
            quantity= StringVar()
            va = 20
            column_heading1 = ["Order ID", "Product ID", "Quantity"]
            for i in column_heading1:
                Label(formframe, text=i, font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
                va += 60
            Entry(formframe, textvariable=order_id, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=102, y=20,height=30)
            Entry(formframe, textvariable=productid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=102, y=80,height=30)
            Entry(formframe, textvariable=quantity, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=102, y=140,height=30)
            Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_order_detail).place(x=10, y=261)
            Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=delete_product_from_detail).place(x=190, y=261)
            Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_record).place(x=370, y=261)
            backbtn = Button(root1, text="Back", font="Georgia 11 bold", bg="white", command=back)
            backbtn.place(x=20, y=40)
                    
            root1.config(bg="sky blue")
            root1.mainloop()

            return None

        def select_order():
            itm = tree.focus()
            if itm == "":
                return None
            else:
                itm = tree.item(itm, "values")
                orderid.set(itm[0])
                platform.set(itm[1])
                processed_chk.set(itm[2])
                packed_chk.set(itm[3])
                sent_chk.set(itm[4])
                returned_chk.set(itm[5])
                money_recieved_chk.set(itm[6])
                orderdate.set(itm[8])
                returndate.set(itm[9])
            return None

        topframe3 = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
        topframe3.place(x=0, y=0)
        title = Label(topframe3, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue",anchor='center')
        title.config(font="Georgia 30 bold")
        title.place(x=320, y=30)

        mainframe3 = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
        mainframe3.place(x=350, y=100)
        welcome = Label(mainframe3, text='Welcome! Update Pending Order Details', fg='white', bg='sky blue',anchor='center')
        welcome.config(font="Georgia 20 bold")
        welcome.place(x=200, y=30)
        backbtn = Button(mainframe3, text="Back", font="Georgia 11 bold", bg="white", command=back)
        backbtn.place(x=50, y=30)

        formframe = Frame(root, width=500, height=480, bg="#FFFFFF")
        formframe.place(x=50, y=285)

        tableframe1 = LabelFrame(root, width=1300, height=400)
        tableframe1.place(x=600, y=285)

        searchframe=Frame(root,width=1000,height=70,bg="sky blue")
        searchframe.place(x=530,y=200)
        searchvar=StringVar()
        searchentry=Entry(searchframe,textvariable=searchvar,font="georgia 15",width=25,bg="white")
        searchentry.place(x=0,y=30,height=40)
        im5 = PhotoImage(file=folder_location + "images\\vieworder.png", master=root)
        im5 = im5.subsample(20, 20)
        search_button = Button(searchframe, text="Search", font="Georgia 11 bold", bg="white",bd=5, image=im5,compound=LEFT, command=search_order)
        search_button.place(x=320, y=30, height=40)
        search_from_form = Button(searchframe, text="Search via Form", font="Georgia 11 bold", bg="white",bd=5, image=im5,compound=LEFT, command=search_using_form_data)
        search_from_form.place(x=420, y=30, height=40)
        order_detail_btn = Button(searchframe, text="Order Details", font="Georgia 11 bold", bg="white",bd=5, image=im5,compound=LEFT, command=double_click)
        order_detail_btn.place(x=760, y=30, height=40)
        include_checkbox_chk = IntVar()
        include_checkbox_chk.set(0)
        cbut4 = Checkbutton(searchframe, text="Include CheckBoxs in Search", font="georgia 11 bold", bg="white",variable=include_checkbox_chk).place(x=420, y=10, anchor="w")

        scrollbarx = Scrollbar(tableframe1, orient=HORIZONTAL)
        scrollbary = Scrollbar(tableframe1, orient=VERTICAL)
        column_width = {"#0": 0, "#1": 70, "#2": 70, "#3": 70, "#4": 70, "#5": 70, "#6": 70, "#7": 100, "#8": 100, "#9": 100, "#10": 100}
        column_heading = ["Order ID", "Platform", "Processed", "Packed", "Sent", "Returned", "Money Recieved", "Total Amount","Order Date","Returned Date"]
        tree = ttk.Treeview(tableframe1, columns=column_heading, selectmode="browse", height=18, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        for i in column_width:
            tree.column(i, stretch=NO, minwidth=0, width=column_width[i])
        for i in column_heading:
            tree.heading(i, text=i, anchor=CENTER)
        tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        tree.bind("<Double-1>", double_click)
        
        formframe.focus_set()
        orderid = StringVar()
        platform = StringVar()
        orderdate = StringVar(value = "YYYY-MM-DD")
        returndate=StringVar(value = "YYYY-MM-DD")
        va = 20
        li = ["Order ID", "Platform", "Order Date"]
        for i in range(3):
            Label(formframe, text=li[i], font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(formframe, textvariable=orderid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=20, height=30)
        Entry(formframe, textvariable=platform, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=80,height=30)
        Entry(formframe, textvariable=orderdate, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=140,height=30)
        processed_chk = IntVar()
        processed_chk.set(0)
        packed_chk = IntVar()
        packed_chk.set(0)
        sent_chk = IntVar()
        sent_chk.set(0)
        returned_chk = IntVar()
        returned_chk.set(0)
        money_recieved_chk=IntVar()
        money_recieved_chk.set(0)
        cbut1 = Checkbutton(formframe, text="Processed", font="georgia 11 bold", bg="white",variable=processed_chk).place(x=80, y=200, anchor="w")
        cbut2 = Checkbutton(formframe, text="Packed", font="georgia 11 bold", bg="white",variable=packed_chk).place(x=200, y=200, anchor="w")
        cbut3 = Checkbutton(formframe, text="Sent", font="georgia 11 bold", bg="white",variable=sent_chk).place(x=80, y=260, anchor="w")
        cbut4 = Checkbutton(formframe, text="Returned", font="georgia 11 bold", bg="white",variable=returned_chk).place(x=140, y=300, anchor="w")
        cbut5 = Checkbutton(formframe, text="Money Recieved", font="georgia 11 bold", bg="white",variable=money_recieved_chk).place(x=200, y=260, anchor="w")
        Label(formframe,text="Returned Date",font="Georgia 11 bold", bg="#FFFFFF").place(x=0,y=340)
        Entry(formframe, textvariable=returndate,font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=340,height=30)
        Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_new_order).place(x=10, y=401)
        Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_order).place(x=130, y=401)
        Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=remove_order).place(x=250, y=401)
        Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_order).place(x=370, y=401)
        root.config(bg="sky blue")
        root.mainloop()

        return None

    def purchases():
        topframe.place_forget()
        mainframe.place_forget()
        buttonframe.place_forget()
        root.title("Purchases Page")

        def back():
            topframe9.place_forget()
            mainframe9.place_forget()
            searchframe.place_forget()
            formframe.place_forget()
            tableframe.place_forget()
            start()
            return None

        def add_new_purchase():
            # purchaseid.get(), item.get(), suppliernumber.get(), quantity.get(), totalamount.get(), paidamount.get(), recieved_chk.get(), placingdate.get(), receiveddate.get(), recievedquantity.get()
            
            if purchaseid.get() == "":
                cursor.execute("SELECT COUNT(*) FROM purchases;")
                purchaseid.set(str(int(cursor.fetchall()[0][0]) + 1))

            for field in [item, suppliernumber, quantity]:
                if field.get() in ["", "Mandatory Entry"]:
                    field.set("Mandatory Entry")
                    return None

            try:
                int(quantity.get())
            except:
                quantity.set("Number Only")
                return None
            
            query = "INSERT INTO purchases VALUES (\"{}\", \"{}\", \"{}\", {}, ".format(purchaseid.get(), item.get(), suppliernumber.get(), quantity.get())

            if totalamount.get() == "":
                totalamount.set("0")

            if paidamount.get() in ["", "Mandatory Entry"]:
                paidamount.set("Mandatory Entry")
                return None
            try:
                int(paidamount.get())
            except:
                paidamount.set("Number Only")
                return None
            
            query += "{}, {}, {}, ".format(totalamount.get(), paidamount.get(), recieved_chk.get())

            if placingdate.get() in ["", "YYYY-MM-DD"]:
                placingdate.set(datetime.datetime.today().strftime('%Y-%m-%d'))
            query += "\"{}\", ".format(placingdate.get())

            if receiveddate.get() in ["", "YYYY-MM-DD"]:
                receiveddate.set("NULL")
                query += "NULL, "
            else:
                query += "\"{}\", ".format(receiveddate.get())

            if recievedquantity.get() == "":
                recievedquantity.set("0")
            else:
                try:
                    int(recievedquantity.get())
                except:
                    recievedquantity.set("Only Number")
                    return None
            query += "{});".format(recievedquantity.get())
            #print(query)
            cursor.execute(query)
            search_purchase()
            return None

        def update_purchase():
            # purchaseid.get(), item.get(), suppliernumber.get(), quantity.get(), totalamount.get(), paidamount.get(), recieved_chk.get(), placingdate.get(), receiveddate.get(), recievedquantity.get()
            query = "UPDATE purchases SET "
            if purchaseid.get() in ["", "Mandatory Entry"]:
                purchaseid.set("Mandatory Entry")
                return None
            
            if item.get() != "":
                query += "ItemID = \"{}\", ".format(item.get())

            if suppliernumber.get() != "":
                query += "SupNo = \"{}\", ".format(suppliernumber.get())

            if quantity.get() != "":
                try:
                    int(quantity.get())
                    query += "Qty = {}, ".format(quantity.get())
                except:
                    quantity.set("Number only")
                    return None
            
            if totalamount.get() != "":
                try:
                    int(totalamount.get())
                    query += "TotalAmount = {}, ".format(totalamount.get())
                except:
                    totalamount.set("Number only")
                    return None
            
            if paidamount.get() != "":
                try:
                    int(paidamount.get())
                    query += "PaidAmount = {}, ".format(paidamount.get())
                except:
                    paidamount.set("Number only")
                    return None
            
            if recieved_chk.get() == 1:
                if receiveddate.get() in ["", "YYY-MM-DD", "None"]:
                    receiveddate.set(datetime.datetime.today().strftime('%Y-%m-%d'))
                query += "Recieved = 1, RecievedDate = \"{}\", ".format(receiveddate.get())
            else:
                query += "Recieved = 0, RecievedDate = NULL, "
            
            if placingdate.get() not in ["", "YYYY-MM-DD"]:
                query += "PlacingDate = \"{}\", ".format(placingdate.get())

            if recievedquantity.get() != "":
                try:
                    int(recievedquantity.get())
                    query += "RecievedQuantity = {}, ".format(recievedquantity.get())
                except:
                    recievedquantity.set("Number only")
                    return None
            
            if query[-4:] != "SET ":
                query = query[:-2] + " WHERE PurchaseID = \"{}\";".format(purchaseid.get())
                print(query)
                cursor.execute(query)
                search_purchase()
            return None

        def remove_purchase():
            if purchaseid.get() in ["", "Mandatory Entry"]:
                purchaseid.set("Mandatory Entry")
            else:
                query = "DELETE FROM purchases WHERE PurchaseID = \"{}\"".format(purchaseid.get())
                cursor.execute(query)
                search_purchase()
            return None

        def select_purchase():
            if tree.focus() != "":
                itm = tree.focus()
                itm = tree.item(itm, "values")
                purchaseid.set(itm[0])
                item.set(itm[1])
                suppliernumber.set(itm[2])
                quantity.set(itm[3])
                totalamount.set(itm[4])
                paidamount.set(itm[5])
                recieved_chk.set(itm[6])
                placingdate.set(itm[7])
                receiveddate.set(itm[8])
                recievedquantity.set(itm[9])
            return None

        def search_purchase():
            query = "SELECT * FROM purchases "
            if searchvar.get() not in ["", "PuchaseID or ItemID or Supplier ID"]:
                query += "WHERE PurchaseID = \"{}\" OR ItemID = \"{}\" OR SupNo = \"{}\";"
                query = query.format(searchvar.get(), searchvar.get(), searchvar.get())
            # print(query)
            cursor.execute(query)
            data = cursor.fetchall()
            put_in_table(tree, data)
            return None

        topframe9 = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
        topframe9.place(x=0, y=0)
        title = Label(topframe9, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue",anchor='center')
        title.config(font="Georgia 30 bold")
        title.place(x=320, y=30)

        mainframe9 = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
        mainframe9.place(x=350, y=80)
        welcome = Label(mainframe9, text='Welcome! Update Existing Purchase Details', fg='white', bg='sky blue',anchor='center')
        welcome.config(font="Georgia 20 bold")
        welcome.place(x=150, y=30)

        searchframe = Frame(root, width=720, height=70, bg="sky blue")
        searchframe.place(x=600, y=170)
        searchvar = StringVar(value="PuchaseID or ItemID or Supplier ID")
        searchentry = Entry(searchframe, textvariable=searchvar, font="georgia 15", width=30, bg="white")
        searchentry.place(x=0, y=20, height=40)
        im = PhotoImage(file = folder_location + "images\\searchdesc.png", master=root)
        im = im.subsample(8, 8)
        searchbtn = Button(searchframe, text="  Search", font="Georgia 11 bold", bg="white", bd=5, image=im,compound=LEFT, command=search_purchase)
        searchbtn.place(x=370, y=20, height=40)

        formframe = Frame(root, width=500, height=500, bg="#FFFFFF")
        formframe.place(x=50, y=240)

        tableframe = LabelFrame(root, width=1300, height=400)
        tableframe.place(x=600, y=240)

        scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(tableframe, orient=VERTICAL)
        column_width = {"#0": 0, "#1": 80, "#2": 50, "#3": 100, "#4": 60, "#5": 80, "#6": 80, "#7": 60, "#8": 80, "#9": 90, "#10": 110}
        column_heading = ["Purchase ID", "Item ID", "Supplier Number", "Quantity", "Total Amount", "Paid Amount","Received","Placing Date","Received Date", "Received Quantity"]
        tree = ttk.Treeview(tableframe, columns=column_heading, selectmode="browse", height=18,yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        for i in column_width:
            tree.column(i, stretch=YES, minwidth=0, width=column_width[i])
        for i in column_heading:
            tree.heading(i, text=i, anchor=CENTER)
        tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        formframe.focus_set()
        purchaseid = StringVar()
        item = StringVar()
        suppliernumber = StringVar()
        quantity = StringVar()
        totalamount = StringVar()
        paidamount = StringVar()
        placingdate = StringVar(value = "YYYY-MM-DD")
        receiveddate = StringVar(value = "YYYY-MM-DD")
        recievedquantity = StringVar()
        va = 5
        li1 = ["Purchase ID", "Item ID", "Supplier Number", "Quantity", "Total Amount", "Paid Amount","Placing Date", "Received Date", "Received Quantity"]
        for i in range(9):
            Label(formframe, text=li1[i], font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 40
        Entry(formframe, textvariable=purchaseid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=5,height=20)
        Entry(formframe, textvariable=item, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=45, height=20)
        Entry(formframe, textvariable=suppliernumber, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=85, height=20)
        Entry(formframe, textvariable=quantity, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=125,height=20)
        Entry(formframe, textvariable=totalamount, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=165,height=20)
        Entry(formframe, textvariable=paidamount, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=205,height=20)
        Entry(formframe, textvariable=placingdate, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=245,height=20)
        Entry(formframe, textvariable=receiveddate, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=285,height=20)
        Entry(formframe, textvariable=recievedquantity, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=325, height=20)
        recieved_chk = IntVar()
        recieved_chk.set(0)
        cbut1 = Checkbutton(formframe, text="Received", font="georgia 11 bold", bg="white",variable=recieved_chk).place(x=142, y=375, anchor="w")
        
        Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_new_purchase).place(x=10, y=400)
        Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_purchase).place(x=130, y=400)
        Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=remove_purchase).place(x=250, y=400)
        Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_purchase).place(x=370, y=400)
        backbtn = Button(root, text="Back", font="Georgia 11 bold", bg="white", command=back)
        backbtn.place(x=400, y=110)
        root.config(bg="sky blue")
        root.mainloop()

        return None

    def supplier_info():
        topframe.place_forget()
        mainframe.place_forget()
        buttonframe.place_forget()
        root.title("Supplier Info")

        def back():
            topframe11.place_forget()
            mainframe11.place_forget()
            formframe.place_forget()
            tableframe.place_forget()
            start()
            pass

        def add_new_supplier():
            if supno.get() in ["", "Mandatory Entry"]:
                cursor.execute("SELECT COUNT(*) FROM supplier;")
                supno.set(str(int(cursor.fetchall()[0][0]) + 1))

            if supname.get() in ["", "Mandatory Entry"]:
                supname.set("Mandatory Entry")
                return None

            if contactno.get() in ["", "Mandatory Entry"]:
                contactno.set("Mandatory Entry")
                return None
            try:
                int(contactno.get()[1:])
            except:
                contactno.set("+91<Numbers and No spaces>")
                return None
            
            query = "INSERT INTO supplier VALUES (\"{}\", \"{}\", \"{}\");".format(supno.get(), supname.get(), contactno.get())
            cursor.execute(query)
            search_supplier()
            return None

        def update_supplier():
            query = "UPDATE supplier SET "
            if supno.get() in ["", "Mandatory Entry"]:
                supno.set("Mandatory Entry")
                return None

            if supname.get() not in ["", "Mandatory Entry"]:
                query += "SupName = \"{}\", ".format(supname.get())

            if contactno.get() not in ["", "Mandatory Entry"]:
                try:
                    int(contactno.get()[1:])
                    query += "ContactNo = \"{}\", ".format(contactno.get())
                except:
                    contactno.set("+91<Numbers and No spaces>")
                    return None

            query = query [:-2] + " WHERE SupNo = \"{}\"".format(supno.get())
            cursor.execute(query)
            search_supplier()
            return None

        def delete_supplier():
            if supno.get() in ["", "Mandatory Entry"]:
                supno.set("Mandatory Entry")
                return None
            
            query = "DELETE FROM supplier WHERE SupNo = \"{}\";".format(supno.get())
            cursor.execute(query)
            search_supplier()
            return None

        def select_supplier():
            if tree.focus() != "":
                itm = tree.focus()
                itm = tree.item(itm, "values")
                supno.set(itm[0])
                supname.set(itm[1])
                contactno.set(itm[2])
            return None

        def search_supplier():
            query = "SELECT * FROM supplier "
            if searchvar.get() not in ["", "SupName or SupNo"]:
                query += "WHERE SupNo LIKE \"%{}%\" OR SupName LIKE \"%{}%\";".format(searchvar.get(), searchvar.get())
            cursor.execute(query)
            data = cursor.fetchall()
            put_in_table(tree, data)
            return None

        topframe11 = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
        topframe11.place(x=0, y=0)
        title = Label(topframe11, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue",anchor='center')
        title.config(font="Georgia 30 bold")
        title.place(x=320, y=30)

        mainframe11 = Frame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
        mainframe11.place(x=350, y=100)
        welcome = Label(mainframe11, text='Welcome! Enter Supplier Details', fg='white', bg='sky blue',anchor='center')
        welcome.config(font="Georgia 20 bold")
        welcome.place(x=200, y=30)
        
        searchframe = Frame(root, width=720, height=70, bg="sky blue")
        searchframe.place(x=400, y=200)
        im = PhotoImage(file = folder_location + "images\\searchdesc.png", master=root)
        im = im.subsample(8, 8)
        backbtn = Button(searchframe, text="Back", font="Georgia 11 bold", bg="white", command=back)
        backbtn.place(x=0, y=20)
        searchvar = StringVar(value="SupName or SupNo")
        searchentry = Entry(searchframe, textvariable=searchvar, font="georgia 15", width=25, bg="white")
        searchentry.place(x=180, y=20, height=40)
        searchbtn = Button(searchframe, text="  Search Item  ", font="Georgia 11 bold", bg="white", bd=5, image=im,compound=LEFT, command=search_supplier)
        searchbtn.place(x=500, y=20, height=40)

        formframe = Frame(root, width=500, height=300, bg="#FFFFFF")
        formframe.place(x=100, y=275)

        tableframe = LabelFrame(root, width=1300, height=400)
        tableframe.place(x=700, y=275)
        scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(tableframe, orient=VERTICAL)
        column_width = {'#0': 0, '#1': 200, '#2': 200, '#3': 200}
        column_heading = ["Supplier Number", "Supplier Name", "Contact Number"]
        tree = ttk.Treeview(tableframe, columns=column_heading,selectmode="browse", height=18, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        for i in column_width:
            tree.column(i, stretch=NO, minwidth=0, width=column_width[i])
        for i in column_heading:
            tree.heading(i, text=i, anchor=CENTER)
        tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        formframe.focus_set()
        supno = StringVar()
        supname = StringVar()
        contactno = StringVar()
        va = 20
        for i in column_heading:
            Label(formframe, text=i, font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(formframe, textvariable=supno, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=20,height=30)
        Entry(formframe, textvariable=supname, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=80,height=30)
        Entry(formframe, textvariable=contactno, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=140,height=30)
            
        Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_new_supplier).place(x=10, y=200)
        Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_supplier).place(x=130, y=200)
        Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=delete_supplier).place(x=250, y=200)
        Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_supplier).place(x=370, y=200)
        
        root.config(bg="sky blue")
        root.mainloop()

        return None

    def products_on_each_platform():
        topframe.place_forget()
        mainframe.place_forget()
        buttonframe.place_forget()
        root.title("Products on Different Platform")

        def search_across_platforms():
            query = "SELECT * FROM products "
            if searchvar.get() not in ["", "ItemID or ProductID or Platform"]:
                query += "WHERE ProductID LIKE \"%{}%\" OR ItemID LIKE \"%{}%\" OR Platform LIKE \"%{}%\" "
                query = query.format(searchvar.get(), searchvar.get(), searchvar.get())
            query += "ORDER BY Platform;"
            print(query)
            cursor.execute(query)
            data = cursor.fetchall()
            put_in_table(tree, data)
            return None

        def back():
            topframe1.place_forget()
            mainframe1.place_forget()
            searchframe.place_forget()
            formframe.place_forget()
            tableframe.place_forget()
            start()
            return None

        def add_to_platform():
            for field in [productid, itemid, platform, sellingprice]:
                if field.get() in ["", "Mandatory Entry"]:
                    field.set("Mandatory Entry")
                    return None
            
            try:
                int(sellingprice.get())
            except:
                sellingprice.set("Number Only")
            
            query = "INSERT INTO products VALUES (\"{}\", \"{}\", \"{}\", {});"
            query = query.format(productid.get(), itemid.get(), platform.get(), sellingprice.get())
            cursor.execute(query)
            search_across_platforms()
            return None

        def update_to_platform():
            if productid.get() in ["", "Mandatory Entry"]:
                productid.set("Mandatory Entry")
                return None
            
            query = "UPDATE products SET "

            if itemid.get() not in ["", "Mandatory Entry"]:
                query += "ItemID = \"{}\", ".format(itemid.get())

            if platform.get() not in ["", "Mandatory Entry"]:
                query += "Platform = \"{}\", ".format(platform.get())
            
            if sellingprice.get() not in ["", "Mandatory Entry"]:
                try:
                    int(sellingprice.get())
                    query += "SellingPrice = {}, ".format(sellingprice.get())
                except:
                    sellingprice.set("Number Only")
                    return None
            
            query = query[:-2] + " WHERE ProductID = \"{}\"".format(productid.get())
            cursor.execute(query)
            search_across_platforms()
            return None

        def delete_from_platform():
            if productid.get() in ["", "Mandatory Entry"]:
                productid.set("Mandatory Entry")
            else:
                query = "DELETE FROM products WHERE ProductID =\"{}\";".format(productid.get())
                cursor.execute(query)
                search_across_platforms()
            return None

        def select_record():
            if tree.focus() != "":
                itm = tree.item(tree.focus(), "values")
                productid.set(itm[0])
                itemid.set(itm[1])
                platform.set(itm[2])
                sellingprice.set(itm[3])
            return None

        topframe1 = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
        topframe1.place(x=0, y=0)
        title = Label(topframe1, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue",anchor='center')
        title.config(font="Georgia 30 bold")
        title.place(x=320, y=30)

        mainframe1 = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
        mainframe1.place(x=350, y=100)
        welcome = Label(mainframe1, text='Welcome to Inventory Page', fg='white', bg='sky blue', anchor='center')
        welcome.config(font="Georgia 20 bold")
        welcome.place(x=200, y=30)

        formframe = Frame(root, width=500, height=450, bg="#FFFFFF")
        formframe.place(x=200, y=275)

        tableframe = LabelFrame(root, width=1300, height=400)
        tableframe.place(x=800, y=275)

        searchframe = Frame(root, width=800, height=70, bg="sky blue")
        searchframe.place(x=300, y=200)
        backbtn = Button(searchframe, text="Back", font="Georgia 11 bold", bg="white", command=back)
        backbtn.place(x=100, y=20, height=40)
        im = PhotoImage(file = folder_location + "images\\searchdesc.png", master=root)
        im = im.subsample(8, 8)
        searchbtn = Button(searchframe, text="Search Item", font="Georgia 11 bold", bg="white", bd=5, image=im,compound=LEFT, command=search_across_platforms)
        searchbtn.place(x=610, y=20, height=40)
        searchvar = StringVar(value="ItemID or ProductID or Platform")
        searchentry = Entry(searchframe, textvariable=searchvar, font="georgia 15", width=25, bg="white")
        searchentry.place(x=300, y=20, height=40)

        scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(tableframe, orient=VERTICAL)
        tree = ttk.Treeview(tableframe,columns=("Product ID", "Item ID", "Platform", "Selling Price"),selectmode="browse", height=18, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        column_width = {"#0": 0, "#1": 100, "#2": 100, "#3": 150, "#4": 150}
        column_heading = ["Product ID", "Item ID", "Platform", "Selling Price"]
        for i in column_width:
            tree.column(i, stretch=YES, minwidth=0, width=column_width[i])
        for i in column_heading:
            tree.heading(i, text=i, anchor=CENTER)
        tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        formframe.focus_set()
        productid = StringVar()
        itemid = StringVar()
        platform = StringVar()
        sellingprice = StringVar()
        va = 20
        for i in range(4):
            Label(formframe, text=column_heading[i], font="Georgia 11 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(formframe, textvariable=productid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=20,height=30)
        Entry(formframe, textvariable=itemid, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=80,height=30)
        Entry(formframe, textvariable=platform, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=140,height=30)
        Entry(formframe, textvariable=sellingprice, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=200,height=30)
        Button(formframe, text="Add", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=add_to_platform).place(x=10, y=361)
        Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_to_platform).place(x=130, y=361)
        Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=delete_from_platform).place(x=250, y=361)
        Button(formframe, text="Select", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=select_record).place(x=370, y=361)
        
        root.config(bg="sky blue")
        root.mainloop()

        return None

    def quit_btn():
        print('Quit')
        if messagebox.askyesno("Quit", " Leave inventory?") == True:
            root.destroy()
            exit(0)
        return None

    topframe = LabelFrame(root, width=2000, height=140, bg="sky blue", borderwidth=0, highlightthickness=0)
    topframe.place(x=0, y=0)
    title = Label(topframe, text='E-Commerce Inventory Management System', fg='snow', bg="sky blue", anchor='center')
    title.config(font="Georgia 30 bold")
    title.place(x=320, y=30)

    mainframe = LabelFrame(root, width=800, height=125, bg='sky blue', borderwidth=0, highlightthickness=0)
    mainframe.place(x=350, y=140)
    welcome = Label(mainframe, text='Welcome to Home Page', fg='white', bg='sky blue', anchor='center')
    welcome.config(font="Georgia 20 bold")
    welcome.place(x=230, y=20)

    buttonframe = LabelFrame(root, width=800, height=300, bg='sky blue', borderwidth=0, highlightthickness=0)
    buttonframe.place(x=450, y=270)
    im = PhotoImage(file = folder_location + "images\\inventory.png", master=root)
    im = im.subsample(8, 8)
    inventory = Button(buttonframe, bd=5, height=80, width= 80, text='Inventory', font='Georgia 11 bold', image=im, compound=TOP,command=inventory_page)
    inventory.place(x=50, y=20)
    im1 = PhotoImage(file = folder_location + "images\\sales.png", master=root)
    im1 = im1.subsample(8, 8)
    sales = Button(buttonframe, bd=5, height=80, width= 80, text='Sales', font='Georgia 11 bold', image=im1, compound=TOP, padx=7,command=sales)
    sales.place(x=250, y=20)
    im2 = PhotoImage(file = folder_location + "images\\salesproj.png", master=root)
    im2 = im2.subsample(4, 4)
    purchases = Button(buttonframe, bd=5, height=80, width= 80, text='Purchases', font='Georgia 11 bold', image=im2, compound=TOP,command=purchases)
    purchases.place(x=450, y=20)
    im4 = PhotoImage(file=folder_location + "images\\supplierinfo.png", master=root)
    im4 = im4.subsample(4, 4)
    supplierinfo = Button(buttonframe, bd=5, height=80, width= 80, text='Suppliers', font='Georgia 11 bold', image=im4, compound=TOP, command=supplier_info)
    supplierinfo.place(x=50, y=170)
    im5=PhotoImage(file=folder_location+"images\\platform.png",master=root)
    im5=im5.subsample(4,4)
    platform=Button(buttonframe, bd=5, width=90, height=80, text='Platform', font='Georgia 11 bold', image=im5, compound=TOP, command=products_on_each_platform)
    platform.place(x=250,y=170)
    im3 = PhotoImage(file = folder_location + "images\\Door_Out-512.png", master=root)
    im3 = im3.subsample(8, 8)
    Quit = Button(buttonframe, bd=5, height=80, width= 80, text='Quit', font='Georgia 11 bold', image=im3, compound=TOP, command=quit_btn)
    Quit.place(x=450, y=170)
    root.config(bg='sky blue')
    root.mainloop()

login_page()