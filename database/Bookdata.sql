INSERT INTO Books (title, isbn, category_id, author_id, publisher, publish_year)
VALUES

(N'Orpheus và Eurydice', 'ISBN-001',
 (SELECT category_id FROM Categories WHERE category_name=N'Thần thoại'),
 (SELECT author_id FROM Authors WHERE author_name=N'Thần thoại Hy Lạp'),
 N'Nhiều bản dịch', -700),

(N'Romeo và Juliet', 'ISBN-002',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'William Shakespeare'),
 N'Oxford', 1597),

(N'Anna Karenina', 'ISBN-003',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Leo Tolstoy'),
 N'Russian Messenger', 1877),

(N'Đồi gió hú', 'ISBN-004',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Emily Brontë'),
 N'Thomas Cautley', 1847),

(N'The Great Gatsby', 'ISBN-005',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'F. Scott Fitzgerald'),
 N'Scribner', 1925),

(N'Những người khốn khổ', 'ISBN-006',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Victor Hugo'),
 N'A. Lacroix', 1862),

(N'1984', 'ISBN-007',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'George Orwell'),
 N'Secker & Warburg', 1949),

(N'Trăm năm cô đơn', 'ISBN-008',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Gabriel García Márquez'),
 N'Sudamericana', 1967),

(N'Kiêu hãnh và định kiến', 'ISBN-009',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Jane Austen'),
 N'T. Egerton', 1813),

(N'Hoàng tử bé', 'ISBN-010',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Antoine de Saint-Exupéry'),
 N'Reynal & Hitchcock', 1943),

(N'Sách văn học số 11','ISBN-011',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Haruki Murakami'),
 N'Shinchosha',1987),

(N'Sách văn học số 12','ISBN-012',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Fyodor Dostoevsky'),
 N'Penguin',1866),

(N'Sách văn học số 13','ISBN-013',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Victor Hugo'),
 N'NXB Văn Học',1860),

(N'Sách văn học số 14','ISBN-014',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Jane Austen'),
 N'Penguin',1815),

(N'Sách văn học số 15','ISBN-015',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'George Orwell'),
 N'Penguin',1945),

(N'Sách tổng hợp 31','ISBN-031',
 (SELECT category_id FROM Categories WHERE category_name=N'Khoa học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Isaac Newton'),
 N'Royal Society',1687),

(N'Sách công nghệ 32','ISBN-032',
 (SELECT category_id FROM Categories WHERE category_name=N'Công nghệ'),
 (SELECT author_id FROM Authors WHERE author_name=N'Robert C. Martin'),
 N'Prentice Hall',2008),

(N'Sách công nghệ 33','ISBN-033',
 (SELECT category_id FROM Categories WHERE category_name=N'Công nghệ'),
 (SELECT author_id FROM Authors WHERE author_name=N'Erich Gamma'),
 N'Addison-Wesley',1994),

(N'Sách khoa học 34','ISBN-034',
 (SELECT category_id FROM Categories WHERE category_name=N'Khoa học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Stephen Hawking'),
 N'Bantam Books',1988),

(N'Sách demo 61','ISBN-061',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2000),

(N'Sách demo 62','ISBN-062',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2005),

(N'Sách demo 63','ISBN-063',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2010),

(N'Sách demo 64','ISBN-064',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2015),

(N'Sách demo 65','ISBN-065',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2020);
