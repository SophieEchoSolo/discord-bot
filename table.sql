CREATE DATABASE IF NOT EXISTS housing;

USE housing;

CREATE TABLE IF NOT EXISTS houses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    street VARCHAR(100),
    region VARCHAR(100),
    rooms INT NOT NULL,
    area INT,
    rent INT NOT NULL,
    story INT,
    applicants INT,
    points INT NOT NULL,
    built INT,
    renovated INT,
    last_app DATETIME,
    date_added DATETIME
);