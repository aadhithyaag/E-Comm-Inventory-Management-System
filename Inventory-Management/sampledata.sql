USE IMS;

insert into supplier values ("1","Rajashri Traders","+919123934346");
insert into supplier values ("2","Saikiran Agencies","+919287118909");
insert into supplier values ("3","AJB Wholesale Store","+919568478587");
insert into supplier values ("4","Jaishankar Traders","+919236542874");

insert into stock values ("1","Wildcrarft E234",90,15,"1");
insert into stock values ("2","Wildcrarft B191",100,20,"1");
insert into stock values ("3","Aristocrat S465",120,10,"2");
insert into stock values ("4","American Tourister A23",200,10,"3");
insert into stock values ("5","American Tourister A46",300,15,"3");
insert into stock values ("6","Adidas Black",100,5,"4");

insert into products values ("A1","1","Amazon","199");
insert into products values ("F1","1","Flipkart","199");
insert into products values ("A2","2","Amazon","239");
insert into products values ("F2","2","Flipkart","249");
insert into products values ("A3","3","Amazon","299");
insert into products values ("F3","3","Flipkart","299");
insert into products values ("A4","4","Amazon","349");
insert into products values ("F4","4","Flipkart","349");
insert into products values ("A5","5","Amazon","499");
insert into products values ("F5","5","Flipkart","499");
insert into products values ("A6","6","Amazon","199");
insert into products values ("F6","6","Flipkart","199");

insert into purchases values("1","1","1",15,0,1350,1,"2021-01-14","2021-01-31",15);
insert into purchases values("2","2","1",20,0,2000,1,"2021-01-14","2021-01-31",20);
insert into purchases values("3","3","2",10,0,1200,1,"2021-01-14","2021-01-30",10);
insert into purchases values("4","4","3",10,0,2000,1,"2021-01-14","2021-01-28",10);
insert into purchases values("5","5","3",15,0,4500,1,"2021-01-14","2021-01-28",15);
insert into purchases values("6","6","4",5,0,500,1,"2021-01-14","2021-01-27",5);


insert into orders (OrderID,Platform,OrderDate) values ("1","Amazon","2021-02-04");
insert into orders (OrderID,Platform,OrderDate) values ("2","Amazon","2021-02-05");
insert into orders (OrderID,Platform,OrderDate) values ("3","Flipkart","2021-02-05");
insert into orders (OrderID,Platform,OrderDate) values ("4","Flipkart","2021-02-06");

insert into order_details (OrderID,ProductID,Qty) values ("1","A1",1);
insert into order_details (OrderID,ProductID,Qty) values ("2","A4",2);
insert into order_details (OrderID,ProductID,Qty) values ("3","F2",1);
insert into order_details (OrderID,ProductID,Qty) values ("4","F3",1);

update orders set Processed=1 where OrderID = "1";
update orders set Processed=1 where OrderID = "2";
update orders set Processed=1 where OrderID = "3";
update orders set Processed=1 where OrderID = "4";

delete FROM stock;
delete from orders;
select * from products;
delete from order_details;
select * from order_details;
delete from purchases;
delete from products;
delete from stock;
delete from supplier;
truncate order_details;