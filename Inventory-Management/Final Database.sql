CREATE DATABASE IMS;

USE IMS;

DROP TABLE IF EXISTS `supplier`;
CREATE TABLE `supplier`(
	`SupNo` CHAR(6) NOT NULL,
    `SupName` VARCHAR(20) NOT NULL,
    `ContactNo` VARCHAR(13) NOT NULL,
    PRIMARY KEY(SupNo)
);
DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock`  (
	`ItemID` VARCHAR(10) NOT NULL,
    `ItemName` VARCHAR(50) NOT NULL,
    `CostPrice` INT NOT NULL,
    `Qty` INT NOT NULL,
    `SupNo` CHAR(6) NOT NULL,
    PRIMARY KEY (`ItemID`),
    FOREIGN KEY (`SupNo`) REFERENCES supplier (`SupNo`)
);
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` ( 
	`ProductID` VARCHAR(10) NOT NULL,
    `ItemID` VARCHAR(10) NOT NULL,
    `Platform` VARCHAR(20) NOT NULL,
    `SellingPrice` INT NOT NULL,
    PRIMARY KEY (`ProductID`),
    FOREIGN KEY (`ItemID`) REFERENCES stock(`ItemID`)
);
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`(
	`OrderID` VARCHAR(20) NOT NULL,
    `Platform`	VARCHAR(20) NOT NULL,
    `Processed` TINYINT NOT NULL DEFAULT 0,
    `Packed` TINYINT NOT NULL DEFAULT 0,
    `Sent` TINYINT NOT NULL DEFAULT 0,
    `Returned` TINYINT NOT NULL DEFAULT 0,
    `MoneyRecieved` TINYINT NOT NULL DEFAULT 0,
    `TotalAmount` INT NOT NULL DEFAULT 0,
	`OrderDate` DATE NOT NULL,
    `ReturnedDate` DATE DEFAULT NULL,
    PRIMARY KEY (`OrderID`)
);
DROP TABLE IF EXISTS `order_details`;
CREATE TABLE `order_details` (
	`OrderID` VARCHAR(20) NOT NULL,
    `ProductID` VARCHAR(10) NOT NULL,
    `Qty` INT NOT NULL,
    `Amount` INT DEFAULT 0,
    FOREIGN KEY (`OrderID`) REFERENCES orders(`OrderID`),
    FOREIGN KEY (`ProductID`) REFERENCES products(`ProductID`)
);

DROP TABLE IF EXISTS `purchases`;
CREATE TABLE `purchases` (
	`PurchaseID` CHAR(10) NOT NULL,
    `ItemID` VARCHAR(10) NOT NULL,
    `SupNo` CHAR(6) NOT NULL,
    `Qty` INT NOT NULL,
    `TotalAmount` INT NOT NULL DEFAULT 0,
    `PaidAmount` INT NOT NULL DEFAULT 0,
    `Recieved` TINYINT NOT NULL DEFAULT 0,
    `PlacingDate` DATE NOT NULL,
    `RecievedDate` DATE DEFAULT NULL,
    `RecievedQuantity` INT DEFAULT NULL,
    PRIMARY KEY(`PurchaseID`),
    FOREIGN KEY(`ItemID`) REFERENCES stock(`ItemID`),
    FOREIGN KEY(`SupNo`) REFERENCES supplier(`SupNo`)
);


DROP TRIGGER IF EXISTS add_stock;
CREATE TRIGGER add_stock
after update
on purchases
FOR EACH ROW
update stock set Qty = Qty + (new.RecievedQuantity - old.RecievedQuantity)
where stock.ItemID = new.ItemID;

DROP TRIGGER IF EXISTS delete_stock;
DELIMITER $$
CREATE TRIGGER delete_stock
after update 
on orders
FOR EACH ROW
BEGIN
	if new.Processed = 1 and old.Processed = 0
    then
    update stock
    set stock.Qty = stock.Qty - (select Qty from order_details,products 
									where order_details.OrderID = new.OrderID
									and products.ProductID = order_details.ProductID
                                    limit 1)
	where stock.ItemID in 
    (select ItemID from products,order_details
    where products.ProductID = order_details.ProductID
	and order_details.OrderID = new.OrderID);
    end if;
END$$

DROP FUNCTION IF EXISTS get_selling_price;
DELIMITER //
CREATE FUNCTION get_selling_price(ProductID  VARCHAR(20)) RETURNS INT DETERMINISTIC
BEGIN
	DECLARE temp INT;
	SET temp=0;
	select SellingPrice into temp from products where ProductID = products.ProductID;
    RETURN temp;
END //
DROP TRIGGER IF EXISTS update_amount;
DELIMITER $$
CREATE TRIGGER update_amount
before insert
on order_details
FOR EACH ROW
set new.Amount = new.Qty * get_selling_price(new.ProductID);

DROP TRIGGER IF EXISTS update_total_amount;
CREATE TRIGGER update_total_amount
after insert 
on order_details
FOR EACH ROW
update orders
set TotalAmount=TotalAmount+new.Amount
where new.OrderID = orders.OrderID;

DROP TRIGGER IF EXISTS reduce_total_amount;
DELIMITER $$
CREATE TRIGGER reduce_total_amount
after delete
on order_details
FOR EACH ROW
update orders
set TotalAmount=TotalAmount-old.Amount
where old.OrderID = orders.OrderID;

DROP FUNCTION IF EXISTS get_cost_price;
DELIMITER //
CREATE FUNCTION get_cost_price(ItemID  VARCHAR(10)) RETURNS INT DETERMINISTIC
BEGIN
	DECLARE temp INT;
	SET temp=0;
	select CostPrice into temp from stock where ItemID = stock.ItemID;
    RETURN temp;
END //
DROP TRIGGER IF EXISTS insert_in_purchase_amount;
DELIMITER $$
CREATE TRIGGER insert_in_purchase_amount
before insert
on purchases
FOR EACH ROW
if new.TotalAmount = 0
then
set new.TotalAmount = new.Qty * get_cost_price(new.ItemID);
end if

DROP TRIGGER IF EXISTS update_purchase_amount;
DELIMITER $$
CREATE TRIGGER update_purchase_amount
before update
on purchases
FOR EACH ROW
if old.TotalAmount = new.TotalAmount
then
if old.Qty != new.Qty or old.ItemID != new.ItemID
then
set new.TotalAmount = new.Qty * get_cost_price(new.ItemID);
end if;
end if;


DROP TRIGGER IF EXISTS update_amount_on_qty_changes;
DELIMITER $$
CREATE TRIGGER update_amount_on_qty_changes
before update 
on order_details
FOR EACH ROW
set new.Amount = new.Qty * get_selling_price(new.ProductID);

DROP TRIGGER IF EXISTS update_total_amount_when_qty_changes;
DELIMITER $$
CREATE TRIGGER update_total_amount_when_qty_changes
after update 
on order_details
FOR EACH ROW
update orders
set TotalAmount=TotalAmount+ (new.Amount-old.Amount)
where new.OrderID = orders.OrderID;
show triggers;