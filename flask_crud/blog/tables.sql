CREATE DATABASE flog_db
USE flog_db

CREATE TABLE user(user_id int auto_increment,
                    first_name varchar(20),
                    last_name varchar(20),
                    username varchar(20) unique,
                    email varchar(30) unique,
                    password varchar(100),
                    primary key(user_id))

CREATE TABLE blog(blog_id int auto_increment,
                    title varchar(100),
                    author varchar(40),
                    created_on date,
                    primary key(blog_id))