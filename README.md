# E-Comm-Inventory-Management-System
Software Application to facilitate management of an Inventory for E-Commerce Retailers

This is a project I did for School in regards to the subject Software Engineering. The idea behind this app is to allow E-Commerce Retailers to keep track of the amount of stock present for each product they sell on multiple E-Commerce platforms such as Flipkart, Amazon and so on. Upon keeping track of the stock present, dead stock (stock which isn't being sold and is present in the inventory for a long time) can be removed and in situtations of natural disasters, stocks can be identified and kept out seperately to hlp the needy.

Interesting Features included are as follows:<br/>
**1. Secure Login through a secret password which is stored in a text file. Text file is further secured by performing encryption using DES Algorithm.**<br/>
**2. User-Friendly interface, easy to understand and use.**<br/>
**3. Details of Products can be viewed through particular search filters based on necessary product details and can be updated if necessary.**<br/>
**4. Information of Suppliers for various products can be viewed and updated if necessary.**<br/>
**5. Order Details from various E-Commerce Platforms can be viewed and updated if necessary.**<br/>
**6. Database consists of triggers which update amount of stocks automatically once any order is sent out for delivery.**<br/><br/>

Modules in the project:<br/>
**1) Login Module**<br/>
-> A text field along with a “Login” button is given. The user must enter the correct password and then they will be taken to the home page.<br/>
-> The home page consists of six buttons namely Inventory to check the stock, Sales to update the order details, Purchases to update purchase details, Supplier to update supplier details, Platform to update product details and Quit for quitting the application. The user can go to the module of their choice by clicking on any of the respective button.<br/>

**2) Stock Module**<br/>
-> In the Inventory Page, the user is provided with a form which has the respective details of an item and text fields in which the details can be entered. Four buttons namely Add, Update, Remove and Select are given to add, update, remove or select an item. A search bar along with a search button is also given to search for a particular item. A tree object is used to display the details of an item or multiple items. A back button is provided to reach the home page.<br/>
-> In the Platform Page, the user is provided with a form which has the respective details of a product and text fields in which the details can be entered. Four buttons namely Add, Update, Remove and Select are given to add, update, remove or select a product. A search bar along with a search button is also given to search for a particular product. A tree object is used to display the details of a product or multiple products. A back button is provided to reach the home page.<br/>

**3) Sales Module**<br/>
-> In the Sales Page, the user is provided with a form which has the respective details of an order and text fields along with checkboxes are provided in which the details can be entered. Four buttons namely Add, Update, Remove and Select are given to add, update, remove or select an order. A search bar along with a search button is also given to search for a particular order. A Search via Form button is also provided to search for orders based on details entered in the form. A tree object is used to display the details of an order or multiple orders. A button is provided to go to the Order Details page. A back button is provided to reach the home page.<br/>
-> In the Order Details Page, the user is provided with a form which has the respective details of a particular order namely Order ID, Product ID and Quantity and text fields have been provided in which the details can be entered. Three buttons namely Add, Remove and Select are given to add, remove and select a particular order and retrieve its details. A search button is also given to search for a particular order’s details. A tree object is used to display the details of an order namely Product ID, Quantity and Amount. A back button is provided to reach the Sales page.<br/>

**4) Purchases Module**<br/>
-> In the Purchases Page, the user is provided with a form which has the respective details of a purchase and text fields along with checkboxes are provided in which the details can be entered. Four buttons namely Add, Update, Remove and Select are given to add, update, remove or select a purchase. A search bar along with a search button is also given to search for a particular purchase. A tree object is used to display the details of a purchase or multiple purchases. A back button is provided to reach the home page.<br/>
-> In the Supplier Page, the user is provided with a form which has the respective details of a particular supplier namely Supplier Number, Supplier Name and Contact Number and text fields have been provided in which the details can be entered. Four buttons namely Add, Update, Remove and Select are given to add, update, remove and select a particular supplier and retrieve their details. A search button is also given to search for a particular supplier’s details. A tree object is used to display the details of a supplier. A back button is provided to reach the home page.<br/><br/>



The whole project is done using Python. Front End User Interface is developed using tkinter module, back-end connection to the database is also done using Python. Database for the project is created using MySQL.
