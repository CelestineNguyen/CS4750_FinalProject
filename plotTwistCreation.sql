-- Creation of Tables and Initial Insertion for CS 4750 Project

-- Celestine Nguyen - haw3wk
-- Fiona Magee - qgt8xq 
-- Jenna Tuohy - mge2zx 
-- Simran Arora - kxt8xt 


-- Create Tables
CREATE TABLE IF NOT EXISTS books(
	book_id INT PRIMARY KEY,
	title TEXT NOT NULL,
	isbn TEXT UNIQUE,
	pages INT,
	date_published DATE,
	description TEXT, 
	average_rating FLOAT,
	cover_image BYTEA
);	

CREATE TABLE IF NOT EXISTS author (
	author_id INT PRIMARY KEY,
	author_name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS book_author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES author(author_id)
);


CREATE TABLE IF NOT EXISTS users (
	user_id INT PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password TEXT,
	email TEXT UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS list_types(
	list_type_id INT PRIMARY KEY,
	type_name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS lists (				 
	list_id INT NOT NULL,
	list_name TEXT,
	list_type_id INT,
	user_id INT,
	PRIMARY KEY (list_id),
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (list_type_id) REFERENCES list_types(list_type_id)
);
	
CREATE TABLE list_books (
    list_id INT,
    book_id INT,
    PRIMARY KEY (list_id, book_id),
    FOREIGN KEY (list_id) REFERENCES lists(list_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


CREATE TABLE IF NOT EXISTS review(
	review_id INT PRIMARY KEY,
book_id INT, 
user_id INT, 
rating INT, 
review_text TEXT, 
created_at DATE,
FOREIGN KEY (book_id) REFERENCES books(book_id),
FOREIGN KEY (user_id) REFERENCES users(user_id),
CONSTRAINT rating_check CHECK (rating >= 0 AND rating <=5)
);
	
CREATE TABLE IF NOT EXISTS nyt_bestsellers (
	nyt_bestsellers_id INT PRIMARY KEY,
	book_id INT NOT NULL, 
	date_nyt DATE NOT NULL, 
	ranking INT NOT NULL,
	FOREIGN KEY (book_id) REFERENCES books(book_id)
);



-- Insert Mock Data
INSERT INTO books (book_id, title, isbn, pages, date_published, description, average_rating, cover_image) VALUES
(1, 'The Midnight Library', '9780525559474', 304, '2020-09-29', 'A woman finds herself in a magical library between life and death, exploring the infinite possibilities of lives she could have lived.', 4.3, 'http://books.google.com/books/content?id=7uqNEAAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'),
(2, 'Project Hail Mary', '9780593135204', 496, '2021-05-04', 'A lone astronaut wakes up with amnesia on a desperate mission to save humanity.', 4.7, 'http://books.google.com/books/content?id=GrYsEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'),
(3, 'Educated', '9780399590504', 352, '2018-02-20', 'A memoir about a woman who grows up in a survivalist family and escapes through education.', 4.5, 'http://books.google.com/books/content?id=2nyNEAAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'),
(4, 'Circe', '9780316556347', 393, '2018-04-10', 'A feminist retelling of the story of Circe, the enchantress from The Odyssey.', 4.4, 'http://books.google.com/books/content?id=W6j2swEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'),
(5, 'The Silent Patient', '9781250301697', 336, '2019-02-05', 'A psychological thriller about a woman who stops speaking after committing a shocking act of violence.', 4.1, 'http://books.google.com/books/content?id=eJjltgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api');


INSERT INTO author (author_id, author_name) VALUES
(1, 'Matt Haig'),
(2, 'Andy Weir'),
(3, 'Tara Westover'),
(4, 'Madeline Miller'),
(5, 'Alex Michaelides');

INSERT INTO book_author(book_id, author_id) VALUES
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
	(5, 5);

INSERT INTO users (user_id, username, password, email) VALUES
(1, 'alice_dev', 'hashedpassword1', 'alice@example.com'),
(2, 'bob_the_builder', 'hashedpassword2', 'bob@example.net'),
(3, 'charlie123', 'hashedpassword3', 'charlie@demo.org'),
(4, 'dana.codes', 'hashedpassword4', 'dana@codingmail.com'),
(5, 'evan_writer', 'hashedpassword5', 'evan@booklovers.io');

INSERT INTO list_types (list_type_id, type_name) VALUES 
(1, 'To Read'),
(2, 'Currently Reading'),
(3, 'Read');

INSERT INTO lists (list_id, user_id, list_name, list_type_id) VALUES
(1, 1, 'Alice''s Sci-Fi Stack', 1),
(2, 2, 'Bob''s Current Reads', 2),
(3, 3, 'Charlie''s Favorites', 3),
(4, 4, 'Dana''s To-Read', 1),
(5, 5, 'Evan''s Cyberpunk Classics', 3);

INSERT INTO list_books (list_id, book_id) VALUES
(1, 2), 
(1, 1), 
(2, 4), 
(2, 5), 
(3, 3), 
(3, 1), 
(4, 3), 
(4, 5),
(5, 4), 
(5, 2); 


INSERT INTO review (review_id, book_id, user_id, rating, review_text, created_at) VALUES
(1, 1, 1, 5, 'Absolutely loved the concept of alternate lives. Very thought-provoking.', '2023-06-15'),
(2, 2, 2, 4, 'Great sci-fi read with a clever twist. Got a bit slow in the middle though.', '2023-07-20'),
(3, 3, 3, 5, 'Incredibly powerful memoir. Couldn''t put it down.', '2023-01-10'),
(4, 4, 4, 4, 'A beautiful retelling of mythology. The writing was lyrical and rich.', '2022-12-02'),
(5, 5, 5, 3, 'Interesting premise but I guessed the twist too early.', '2023-02-17'),
(6, 2, 1, 5, 'Andy Weir does it again! Funny, smart, and nerdy in the best way.', '2023-08-01'),
(7, 1, 3, 4, 'A good read. Helped me reflect on life choices in a unique way.', '2023-04-25');

INSERT INTO nyt_bestsellers (nyt_bestsellers_id, book_id, date_nyt, ranking) VALUES
(1, 1, '2025-03-23', 1),  
(2, 2, '2025-03-23', 2),  
(3, 3, '2025-03-23', 3);  

-- Views
-- referenced: https://neon.tech/postgresql/postgresql-aggregate-functions/postgresql-string_agg-function
CREATE VIEW book_details AS
SELECT 
    b.book_id, 
    b.title, 
    b.isbn, 
    b.pages, 
    b.date_published, 
    b.description, 
    b.average_rating, 
    STRING_AGG(a.author_name, ', ') AS authors
FROM books b
JOIN book_author ba ON b.book_id = ba.book_id
JOIN author a ON ba.author_id = a.author_id
GROUP BY b.book_id;

CREATE VIEW user_reviews AS
SELECT 
    r.review_id, 
    u.username, 
    b.title AS book_title, 
    r.rating, 
    r.review_text, 
    r.created_at
FROM review r
JOIN users u ON r.user_id = u.user_id
JOIN books b ON r.book_id = b.book_id;


CREATE VIEW nyt_books AS
SELECT 
    n.nyt_bestsellers_id, 
    b.title, 
    b.isbn, 
    n.date_nyt, 
    n.ranking
FROM nyt_bestsellers n
JOIN books b ON n.book_id = b.book_id;
	

CREATE VIEW owner_booklist_and_rating AS
SELECT 
    l.list_id,
    l.list_name,
    lt.type_name AS list_type, 
    u.username AS list_owner,
    COALESCE(STRING_AGG(DISTINCT b.title, ', '), 'No Books in List') AS books,
    COALESCE(STRING_AGG(DISTINCT b.book_id::TEXT, ', '), 'No Books') AS book_ids,
    COALESCE(STRING_AGG(DISTINCT r.rating::TEXT, ', '), NULL) AS owner_ratings,
    COALESCE(AVG(r.rating)::NUMERIC(3,1), NULL) AS avg_owner_rating
FROM lists l
JOIN list_types lt ON l.list_type_id = lt.list_type_id
JOIN users u ON l.user_id = u.user_id
LEFT JOIN list_books lb ON l.list_id = lb.list_id
LEFT JOIN books b ON lb.book_id = b.book_id
LEFT JOIN review r ON b.book_id = r.book_id AND r.user_id = l.user_id 
GROUP BY l.list_id, lt.type_name, u.username;

CREATE VIEW per_row_owner_booklist_and_rating AS
SELECT 
    l.list_id,
    l.list_name,
    lt.type_name AS list_type, 
    u.username AS list_owner,
    b.book_id,
    b.title AS book_title,
    r.rating AS owner_rating 
FROM lists l
JOIN list_types lt ON l.list_type_id = lt.list_type_id
JOIN users u ON l.user_id = u.user_id
LEFT JOIN list_books lb ON l.list_id = lb.list_id
LEFT JOIN books b ON lb.book_id = b.book_id
LEFT JOIN review r ON b.book_id = r.book_id AND r.user_id = l.user_id;

-- alter table to make email optional
ALTER TABLE users ALTER COLUMN email DROP NOT NULL;
-- Remove the UNIQUE constraint from the email column
ALTER TABLE users DROP CONSTRAINT users_email_key;


-- create trigger to add new user after registration
CREATE OR REPLACE FUNCTION sync_auth_user_to_users()
RETURNS trigger AS $$
BEGIN
    INSERT INTO users (user_id, username, password, email)
    VALUES (NEW.id, NEW.username, NEW.password, NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_sync_auth_user
AFTER INSERT ON auth_user
FOR EACH ROW
EXECUTE FUNCTION sync_auth_user_to_users();

