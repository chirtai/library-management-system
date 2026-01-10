CREATE DATABASE LibraryManagement;
USE LibraryManagement;


CREATE TABLE Categories (
    category_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Authors (
    author_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(150) NOT NULL,
    bio TEXT
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    role VARCHAR(20) DEFAULT 'MEMBER' 
        CHECK (role IN ('ADMIN', 'LIBRARIAN', 'MEMBER')),
    status VARCHAR(20) DEFAULT 'PENDING' 
        CHECK (status IN ('PENDING', 'ACTIVE', 'INACTIVE', 'BLOCKED')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Books (
    book_id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    category_id INT,
    author_id INT,
    publisher VARCHAR(100),
    publish_year INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);

CREATE TABLE BookCopies (
    copy_id INT PRIMARY KEY IDENTITY(1,1),
    book_id INT,
    barcode VARCHAR(50) UNIQUE, 
     status VARCHAR(20) DEFAULT 'AVAILABLE' 
        CHECK (status IN ('AVAILABLE', 'BORROWED', 'LOST', 'MAINTENANCE')),
    location VARCHAR(50),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);


CREATE TABLE Borrowing (
    borrow_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT, 
    copy_id INT, 
    staff_id INT, 
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL, 
    return_date DATE, 
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (copy_id) REFERENCES BookCopies(copy_id),
    FOREIGN KEY (staff_id) REFERENCES Users(user_id)
);

CREATE TABLE Fines (
    fine_id INT PRIMARY KEY IDENTITY(1,1),
    borrow_id INT,
    amount DECIMAL(10,2),
    reason TEXT,
    payment_status NVARCHAR(20) DEFAULT 'UNPAID' 
        CHECK (payment_status IN ('UNPAID', 'PAID')),
    FOREIGN KEY (borrow_id) REFERENCES Borrowing(borrow_id)
);

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY IDENTITY(1,1),
    fine_id INT, 
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL 
		CHECK (payment_method IN ('CASH', 'BANK_TRANSFER', 'MOMO', 'CREDIT_CARD')), 
    transaction_no VARCHAR(100), 
    staff_id INT, 
    FOREIGN KEY (fine_id) REFERENCES Fines(fine_id),
    FOREIGN KEY (staff_id) REFERENCES Users(user_id)
);

