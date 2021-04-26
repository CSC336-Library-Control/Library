DROP DATABASE IF EXISTS Library;
CREATE DATABASE Library;

USE Library;

DROP TABLE if EXISTS Login;
CREATE TABLE Login(
    UserID VARCHAR(32) PRIMARY KEY,
    PASSWORD VARCHAR(32) NOT NULL,
    Role ENUM('User','Staff') NOT NULL
);

DROP TABLE if EXISTS Books;
CREATE TABLE Books(
    ISBN VARCHAR(32) PRIMARY KEY,
    Title VARCHAR(64) NOT NULL,
    Copies INTEGER NOT NULL,
    PublicationDate VARCHAR(32),
    Author VARCHAR(32) NOT NULL,
    Image VARCHAR(32),
    REMOVE ENUM('True', 'False') DEFAULT 'False'
);

DROP TABLE if EXISTS User;
CREATE TABLE User(
    UserID VARCHAR(32) PRIMARY KEY,
    NAME VARCHAR(32),
    BirthDate VARCHAR(32),
    Email VARCHAR(32),
    Phone VARCHAR(32),
    Address VARCHAR(32),
    FOREIGN KEY(UserID) REFERENCES Login(UserID)
);

DROP TABLE if EXISTS BorrowRecord;
CREATE TABLE BorrowRecord(
    BorrowID INTEGER PRIMARY KEY AUTO_INCREMENT,
    UserID VARCHAR(32) NOT NULL,
    ISBN VARCHAR(32) NOT NULL,
    BorrowDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DueDate TIMESTAMP,
    StaffID VARCHAR(32) NOT NULL,
    Returned ENUM('True', 'False') NOT NULL,
    FOREIGN KEY(UserID) REFERENCES User(UserID),
    FOREIGN KEY(ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY(StaffID) REFERENCES User(UserID)
);

CREATE TRIGGER due_date BEFORE INSERT ON BorrowRecord
FOR EACH ROW SET
    NEW.DueDate = TIMESTAMPADD(DAY, 14, NEW.BorrowDate),
    NEW.Returned = 'False';


DROP TABLE if EXISTS ReturnRecord;
CREATE TABLE ReturnRecord(
    BorrowID INTEGER PRIMARY KEY,
    ReturnDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    StaffID VARCHAR(32),
    Issue VARCHAR(64),
    FOREIGN KEY(BorrowID) REFERENCES BorrowRecord(BorrowID),
    FOREIGN KEY(StaffID) REFERENCES User(UserID)
);

DROP TABLE if EXISTS OrderRecord;
CREATE TABLE OrderRecord(
    OrderID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ISBN VARCHAR(32) NOT NULL,
    UserID VARCHAR(32) NOT NULL,
    DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    STATUS ENUM('Waiting', 'Canceled', 'Completed') NOT NULL,
    FOREIGN KEY(ISBN) REFERENCES books(ISBN),
    FOREIGN KEY(UserID) REFERENCES User(UserID)
);

CREATE TRIGGER order_status BEFORE INSERT ON OrderRecord
FOR EACH ROW SET
    NEW.STATUS = 'Waiting';

    
INSERT INTO Login VALUES ('User1', '000000', 'User');
INSERT INTO Login VALUES ('User2', '000000', 'User');
INSERT INTO Login VALUES ('User3', '000000', 'User');
INSERT INTO Login VALUES ('User4', '000000', 'User');

INSERT INTO Login VALUES ('Staff1', '000000', 'Staff');
INSERT INTO Login VALUES ('Staff2', '000000', 'Staff');

INSERT INTO User(UserID, NAME) VALUES ('User1', 'User1');
INSERT INTO User(UserID, NAME) VALUES ('User2', 'User2');
INSERT INTO User(UserID, NAME) VALUES ('User3', 'User3');
INSERT INTO User(UserID, NAME) VALUES ('User4', 'User4');
INSERT INTO User(UserID, NAME) VALUES ('Staff1', 'Staff1');
INSERT INTO User(UserID, NAME) VALUES ('Staff2', 'Staff2');

SELECT * FROM Login;
SELECT * FROM USER;

INSERT INTO Books VALUES('1250178606', 'The Four Winds: A Novel', 8, '2021-02-02', 'Kristin Hannah', '1250178606.jpg', 'False');
INSERT INTO Books VALUES('0735219095', 'Where the Crawdads Sing', 4, '2018-08-14', 'Delia Owens', '0735219095.jpg','False');
INSERT INTO Books VALUES('0525559477', 'The Midnight Library: A Novel', 6, '2020-09-29', 'Matt Haig', '0525559477.jpg','False');
INSERT INTO Books VALUES('1635640520', 'The Cedar Key ', 6, '2020-09-06', 'Stephenia H. McGee', '1635640520.jpg','False');
INSERT INTO Books VALUES('0525536299', 'The Vanishing Half: A Novel', 6, '2020-06-02', 'Brit Bennett', '0525536299.jpg','False');
INSERT INTO Books VALUES('0593128176', 'The Beekeeper of Aleppo: A Novel', 6, '2020-06-23', 'Christy Lefteri ', '0593128176.jpg','False');
INSERT INTO Books VALUES('1455563920', 'Pachinko', 6, '2017-11-14', 'Min Jin Lee', '1455563920.jpg','False');
INSERT INTO Books VALUES('153871485X', 'Free Food for Millionaires ', 6, '2018-06-05', 'Min Jin Lee', '153871485X.jpg','False');
INSERT INTO Books VALUES('1984819887', 'The Book of Lost Friends: A Novel', 6, '2020-04-07', 'Lisa Wingate', '1984819887.jpg','False');
INSERT INTO Books VALUES('1524763136', 'Becoming', 6, '2018-11-13', 'Michelle Obama', '1524763136.jpg','False');


SELECT * FROM Books;

INSERT INTO BorrowRecord(UserID, ISBN, StaffID) VALUES ('User1', '1250178606', 'Staff1');

SELECT * FROM borrowrecord;

INSERT INTO OrderRecord(UserID, ISBN) VALUES ('User1', '1250178606');
INSERT INTO OrderRecord(UserID, ISBN) VALUES ('User2', '1250178606');

SELECT * FROM OrderRecord;
