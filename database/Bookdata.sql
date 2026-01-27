INSERT INTO Books (title, isbn, category_id, author_id, publisher, publish_year)
VALUES
(N'Orpheus và Eurydice','ISBN-001',
 (SELECT category_id FROM Categories WHERE category_name=N'Thần thoại'),
 (SELECT author_id FROM Authors WHERE author_name=N'Thần thoại Hy Lạp'),
 N'Nhiều bản dịch',-700),

(N'Romeo và Juliet','ISBN-002',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'William Shakespeare'),
 N'Oxford',1597),

(N'Tristan và Iseult','ISBN-003',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Victor Hugo'),
 N'Penguin',1200),

(N'Anna Karenina','ISBN-004',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Leo Tolstoy'),
 N'Russian Messenger',1877),

(N'Đồi gió hú','ISBN-005',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Emily Brontë'),
 N'Thomas Cautley',1847),

(N'Kiêu hãnh và định kiến','ISBN-006',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'Jane Austen'),
 N'Penguin',1813),

(N'The Great Gatsby','ISBN-007',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học tình yêu'),
 (SELECT author_id FROM Authors WHERE author_name=N'F. Scott Fitzgerald'),
 N'Scribner',1925),

(N'Trăm năm cô đơn','ISBN-008',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Gabriel García Márquez'),
 N'Sudamericana',1967),

(N'1984','ISBN-009',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'George Orwell'),
 N'Secker & Warburg',1949),

(N'Những người khốn khổ','ISBN-010',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Victor Hugo'),
 N'A. Lacroix',1862),

-- 11–50 Sách ngẫu nhiên văn học
(N'Sách văn học 11','ISBN-011',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Haruki Murakami'),
 N'Shinchosha',1987),

(N'Sách văn học 12','ISBN-012',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Fyodor Dostoevsky'),
 N'Penguin',1866),

(N'Sách văn học 13','ISBN-013',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2001),

(N'Sách văn học 14','ISBN-014',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2005),

(N'Sách văn học 15','ISBN-015',
 (SELECT category_id FROM Categories WHERE category_name=N'Văn học'),
 (SELECT author_id FROM Authors WHERE author_name=N'Nguyễn Nhật Ánh'),
 N'NXB Trẻ',2010);



