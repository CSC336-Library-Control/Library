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
    Title VARCHAR(32) NOT NULL,
    Copies INTEGER NOT NULL,
    PublicationDate VARCHAR(32),
    Author VARCHAR(32) NOT NULL,
    Image VARCHAR(64),
    REMOVE ENUM('True', 'False') DEFAULT 'False'
);

DROP TABLE if EXISTS USER;
CREATE TABLE USER(
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
    FOREIGN KEY(UserID) REFERENCES USER(UserID),
    FOREIGN KEY(ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY(StaffID) REFERENCES USER(UserID)
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
    FOREIGN KEY(UserID) REFERENCES user(UserID)
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

INSERT INTO USER(UserID, NAME) VALUES ('User1', 'User1');
INSERT INTO USER(UserID, NAME) VALUES ('User2', 'User2');
INSERT INTO USER(UserID, NAME) VALUES ('User3', 'User3');
INSERT INTO USER(UserID, NAME) VALUES ('User4', 'User4');
INSERT INTO USER(UserID, NAME) VALUES ('Staff1', 'Staff1');
INSERT INTO USER(UserID, NAME) VALUES ('Staff2', 'Staff2');

SELECT * FROM Login;
SELECT * FROM USER;

INSERT INTO Books(ISBN, Title, Copies, Author) VALUES ('isbn1', 'book1', 3, 'author1');
INSERT INTO Books(ISBN, Title, Copies, Author) VALUES ('isbn2', 'book2', 3, 'author2');
INSERT INTO Books(ISBN, Title, Copies, Author) VALUES ('isbn3', 'book3', 3, 'author3');
INSERT INTO Books(ISBN, Title, Copies, Author) VALUES ('isbn4', 'book4', 3, 'author4');

SELECT * FROM Books;

INSERT INTO BorrowRecord(UserID, ISBN, StaffID) VALUES ('User1', 'isbn1', 'Staff1');

SELECT * FROM borrowrecord;

INSERT INTO OrderRecord(UserID, ISBN) VALUES ('User1', 'isbn1');
INSERT INTO OrderRecord(UserID, ISBN) VALUES ('User2', 'isbn1');

SELECT * FROM OrderRecord;