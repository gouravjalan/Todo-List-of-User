CREATE DATABASE todo_db;
USE todo_db;

CREATE TABLE users(
	id int auto_increment primary key,
    name varchar(100),
    email varchar(100) unique,
    password varchar(100)
    );
    
    
CREATE TABLE todo_list(
	id int auto_increment primary key,
    title varchar(255),
    description varchar(255),
    completed BOOLEAN DEFAULT FALSE,
    user_id int,
    FOREIGN KEY (user_id) REFERENCES users(id)
    );
    
    
SHOW TABLES;
DESCRIBE users;
DESCRIBE todo_list;

ALTER TABLE users MODIFY password VARCHAR(255), MODIFY name VARCHAR(255), MODIFY email VARCHAR(255);
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE todo_list AUTO_INCREMENT = 1;


-- The below 4 steps will clear the rows of both table but the columns will become empty and id will start again from 1.
	SET FOREIGN_KEY_CHECKS = 0;
    TRUNCATE TABLE todo_list;
    TRUNCATE TABLE users;
    SET FOREIGN_KEY_CHECKS = 1;
    
-- bydefault a new table was created with name below bcoz in python code name was inappropriate, so to delete that table
	DROP TABLE todos;
    
-- if anything goes wrong so to update the changes in table, used this 
    SET SQL_SAFE_UPDATES=0;
    DELETE FROM todo_list;
    DELETE FROM users;
    SET SQL_SAFE_UPDATES=1;
    
-- below r steps to create uuid in existing database.
    ALTER TABLE todo_list DROP FOREIGN KEY todo_list_ibfk_1; -- the name was shown in error
    
-- to change id in users to uuid
    ALTER TABLE users MODIFY COLUMN id CHAR(36);
-- uuid basically is 36 bit in size, so char is 36

-- to change id in todolist to uuid
    ALTER TABLE todo_list MODIFY COLUMN id CHAR(36);
-- uuid basically is 36 bit in size, so char is 36

-- to change userid in todolist to uuid
    ALTER TABLE todo_list MODIFY COLUMN user_id CHAR(36);
-- uuid basically is 36 bit in size, so char is 36
    
-- created foreignkey again as we need it and it will be same as id in users table.
    ALTER TABLE todo_list ADD CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id);

-- to change (int)id to uuid we use this.
    UPDATE users SET id = UUID() WHERE id REGEXP '^[0-9]+$';
-- only the integer id users will be changed to uuid by use of this
-- ^ represent the start
-- [0-9] is the range of numbers that r present in uuid
-- $ is the end of id
    
-- to change the existing id(int) to uuid(str)
	-- ALTER TABLE users ADD COLUMN old_id INT;
	-- ALTER TABLE users MODIFY old_id CHAR(36);
	-- UPDATE users SET old_id = id;
	-- ALTER TABLE users DROP COLUMN old_id;
    
-- Below 2 queries are for the functionality of soft delete
-- 0 for user exist in table and 1 for user is deleted from table.
-- ALTER TABLE users ADD COLUMN is_deleted BOOLEAN DEFAULT 0;
-- UPDATE users SET is_deleted = 1 WHERE id ='uuid';

-- below query is to soft delete the user todo list 
-- ALTER TABLE users DROP COLUMN is_deleted;

-- below table for the functionality of soft delete
ALTER TABLE todo_list ADD COLUMN is_deleted_check BOOLEAN DEFAULT 0;
-- ALTER TABLE todo_list DROP COLUMN is_deleted;

ALTER TABLE users ADD COLUMN role ENUM('user', 'admin') DEFAULT 'user';
ALTER TABLE users DROP COLUMN role;

-- to make a user admin after login via db only manually
UPDATE users SET role='admin' WHERE email='rashi02@gmail.com';
UPDATE users SET role='admin' WHERE email='viratkohli@gmail.com';
UPDATE users SET role='admin' WHERE email='msdhoni1997@gmail.com';

select * from users;
select * from todo_list;
