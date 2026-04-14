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

DELETE FROM users WHERE id = '3bf7f20f-16aa-4b1a-9bb3-80634210153d';

DELETE FROM users WHERE id = '044676ac-5980-4cd4-b03e-22591328f708';
DELETE FROM users WHERE id = '0b7c5091-dfde-44cc-b279-f970a9a64063';
DELETE FROM users WHERE id = '6f51e703-ce24-4428-969b-de5a2cc682f5';
DELETE FROM users WHERE id = 'df6c830e-a57f-4fff-bd1b-dec43b7bd7d6';
DELETE FROM users WHERE id = 'bf2f51d5-34d7-4a11-b909-e2038876e51f';
DELETE FROM users WHERE id = 'ad768d12-0084-48f6-a332-5fb5e447d356';

DELETE FROM users WHERE id = '134b11f6-38fc-4fe3-9c8b-b38110f8d21c';
DELETE FROM users WHERE id = '621b14b4-f1d4-436b-9781-97fd9410dc71';
DELETE FROM users WHERE id = 'b0392904-c419-4ff9-a1c1-bbd726fedcbd';
DELETE FROM users WHERE id = 'c1987c50-4629-4434-906d-d9cd82225982';
DELETE FROM users WHERE id = 'd263b016-47b1-49e5-a30a-7db7e913f20f';
DELETE FROM users WHERE id = 'daf683e6-0e0d-4758-9c79-14bd19071bf9';
DELETE FROM users WHERE id = 'e0cb2684-f5b5-49da-af2f-6ef173357479';

DELETE FROM users WHERE id = '5d67b74d-c2e6-4bce-aca0-c523b48ee00b';
DELETE FROM users WHERE id = '621a8c6b-be51-43ae-aa3d-fe8890eef52b';
DELETE FROM users WHERE id = '81fdd964-4ab2-4245-bd60-3df08fb3e9de';
DELETE FROM users WHERE id = '4393aaf1-636c-4807-841d-44bc0cd0349c';
DELETE FROM users WHERE id = '4eefbe23-1414-49bd-95b8-f7b4765d5601';
DELETE FROM users WHERE id = 'ed480a51-1558-4c99-a489-ed78b54dc4e4';
DELETE FROM users WHERE id = '367c6a33-5003-4cf3-8d81-f4e0daa47d4b';

DELETE FROM users WHERE id = 'cdf77685-70f1-4024-908c-e6b388857951';
DELETE FROM users WHERE id = 'f5e4eaea-4339-402e-9fbf-700159ec38c7';
DELETE FROM users WHERE id = 'acf60103-e610-49bc-98b0-a547848a2d45';
DELETE FROM users WHERE id = '3a6dd7d6-38fb-4681-b9a1-9f0d233cc579';
DELETE FROM users WHERE id = '1899759a-3c65-4bcd-bd88-b2e967361024';
DELETE FROM users WHERE id = '0f8a18f6-7bea-42c4-a895-c5152e87aa7a';

DELETE FROM todo_list WHERE id = '8878afd6-0334-44c1-b7aa-dd94503386e7';
DELETE FROM users WHERE id = '5e2a3e86-8128-402d-8643-96e2b62f6e91';

DELETE FROM todo_list WHERE id = 'cd3f9ef7-5978-495a-8046-701150bd3caa';
DELETE FROM todo_list WHERE id = '6c5b1ae7-7cd8-47aa-8be4-8473b0f9bdfd';
DELETE FROM todo_list WHERE id = '4e9835cf-a45e-4efc-845c-b0b4abe4bedf';

DELETE FROM todo_list WHERE id = '178c15f0-dce9-4e16-a05f-a0716d0aedf1';

DELETE FROM todo_list WHERE id = '207a3007-dc30-4cb0-8332-8e230fb41696';
DELETE FROM todo_list WHERE id = '5ffa598e-c06a-4993-a824-d20e19393511';
DELETE FROM todo_list WHERE id = '99a6d6d3-aacb-43bd-aa26-f33da8bd0352';

DELETE FROM todo_list WHERE id = 'a9a4c032-594f-4b96-b7da-63062fdc2d87';
DELETE FROM todo_list WHERE id = 'b581a2e6-54a8-420b-b4cb-54b56648d36e';
DELETE FROM todo_list WHERE id = 'c73cac15-cf07-47bf-9d86-6819447a62b3';
DELETE FROM todo_list WHERE id = 'c8a4e5d3-860c-4be8-9889-2b0554949e5d';
DELETE FROM todo_list WHERE id = 'd7cc6984-6354-4594-8b67-c7f70e966730';
DELETE FROM todo_list WHERE id = '50ed0c1e-b51e-48c1-a313-1b0602241606';

DELETE FROM user_role WHERE role_id = '9a75c1f1-3946-47b7-a34e-4a652e26eaf6';
DELETE FROM user_role WHERE role_id = '0d564813-ab03-4269-8d84-f07ec1bee441';
DELETE FROM user_role WHERE role_id = '02d14037-3701-11f1-8eed-9cc7d3fcf7af';
DELETE FROM user_role WHERE role_id = 'ae5798c6-7618-4d25-8c39-6c7919007250';

select * from users;
select * from todo_list;
select * from user_role;

INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'user', '048a7eee-fc7e-4d2f-9531-d9cb64dc9987');
INSERT INTO user_role (role_id, role, user_id) VALUES (UUID(), 'admin', 'a8638be6-a728-4989-b7cf-da4b77340afa');
INSERT INTO user_role (role_id,role,user_id) VALUES (UUID(),'admin','3951f476-5775-4eec-aac6-963748f232c5');
INSERT INTO user_role (role_id,role,user_id) VALUES (UUID(),'user','3852621d-ce11-40aa-9f4f-3f22a32bc579');


-- 2bf684ba-51d4-448a-bdee-88c16c52a3dc