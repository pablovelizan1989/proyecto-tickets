CREATE DATABASE tickets_db;
USE tickets_db;

CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    categoria VARCHAR(50),
    cantidad INT,
    total DECIMAL(10,2),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    categoria VARCHAR(50),
    cantidad INT,
    total DECIMAL(10,2),
    fecha DATETIME
);
