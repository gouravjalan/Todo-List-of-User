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
    
CREATE TABLE user_role(
	role_id CHAR(36) PRIMARY KEY,
    role ENUM ('admin','user'),
    user_role_id CHAR(36),
    FOREIGN KEY (user_role_id) REFERENCES users(id)
    );
    
SHOW TABLES;
DESCRIBE users;
DESCRIBE todo_list;
DESCRIBE user_role; 

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

UPDATE users SET role='admin' WHERE email='sachin100@gmial.com';
UPDATE users SET role='admin' WHERE email='gsjalan@gmail.com';

UPDATE users SET email = 'sachin100@gmail.com' WHERE id = 'ad768d12-0084-48f6-a332-5fb5e447d356';

ALTER TABLE users DROP COLUMN role;

-- To check if the user_role table is accepting data
INSERT INTO user_role (role_id, role, user_role_id) VALUES (UUID(), 'admin', 'acf60103-e610-49bc-98b0-a547848a2d45');
INSERT INTO user_role (role_id, role, user_role_id) VALUES (UUID(), 'admin', '0b7c5091-dfde-44cc-b279-f970a9a64063');

-- updated the name of user_role_id to user_id now
INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'admin', 'fad4daf3-1b02-4917-965e-f54d64b5a8e4');
INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'admin', 'a28b4931-3ed0-4ba5-85aa-94a67bbd2fe6');


SELECT * FROM user_role WHERE user_role_id = 'cdf77685-70f1-4024-908c-e6b388857951';

-- changed the name of user_role_id to user_id bcoz of naming mismatch for python as it uses user_id
ALTER TABLE user_role CHANGE user_role_id user_id CHAR(36);


DELETE FROM user_role;
TRUNCATE TABLE user_role;

DELETE FROM todo_list WHERE id = '8878afd6-0334-44c1-b7aa-dd94503386e7';
DELETE FROM users WHERE id = '5e2a3e86-8128-402d-8643-96e2b62f6e91';


INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'user', '048a7eee-fc7e-4d2f-9531-d9cb64dc9987');
INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'admin', 'a8638be6-a728-4989-b7cf-da4b77340afa');
INSERT INTO user_role (role_id,role,user_id) VALUES (UUID(),'admin','3951f476-5775-4eec-aac6-963748f232c5');
INSERT INTO user_role (role_id,role,user_id) VALUES (UUID(),'user','3852621d-ce11-40aa-9f4f-3f22a32bc579');

-- To add the 3 more columns in existing tables
ALTER TABLE users ADD COLUMN created_at TIMESTAMP;
ALTER TABLE users ADD COLUMN modified_at TIMESTAMP;
ALTER TABLE users ADD COLUMN modified_by VARCHAR(36);


ALTER TABLE todo_list ADD COLUMN created_at TIMESTAMP;
ALTER TABLE todo_list ADD COLUMN modified_at TIMESTAMP;
ALTER TABLE todo_list ADD COLUMN modified_by VARCHAR(36);


ALTER TABLE user_role ADD COLUMN created_at TIMESTAMP;
ALTER TABLE user_role ADD COLUMN modified_at TIMESTAMP;
ALTER TABLE user_role ADD COLUMN modified_by VARCHAR(36);


select * from users;
select * from todo_list;
select * from user_role;

