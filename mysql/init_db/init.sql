CREATE DATABASE tikiDB;
USE tikiDB;
CREATE TABLE parentCategory(
    parentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cateName VARCHAR(150) NOT NULL,
    urlKey VARCHAR(150) NOT NULL,
    iconURL VARCHAR(500) NOT NULL
);
CREATE TABLE childCategory (
    childID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cateName NVARCHAR(150) NOT NULL,
    urlKey VARCHAR(150) NOT NULL,
    parentID INT NOT NULL,
    FOREIGN KEY (parentID) REFERENCES parentCategory(parentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE productCate(
    productID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(150) NOT NULL,
    price INT,
    quantitySold INT,
    imgURL VARCHAR(500),
    childID INT NOT NULL,
    FOREIGN KEY (childID) REFERENCES childCategory(childID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    parentID INT NOT NULL,
    FOREIGN KEY (parentID) REFERENCES parentCategory(parentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    
)
