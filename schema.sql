-- Database Schema for Library Management
CREATE DATABASE IF NOT EXISTS `library_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `library_db`;

CREATE TABLE IF NOT EXISTS `books` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(255) NOT NULL,
    `category` VARCHAR(100) NOT NULL,
    `total` INT DEFAULT 1,
    `available` INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS `members` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `phone` VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS `borrows` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `book_id` INT NOT NULL,
    `member_id` INT NOT NULL,
    `borrow_date` DATE NOT NULL,
    `due_date` DATE NOT NULL,
    `return_date` DATE NULL,
    `fine_amount` INT DEFAULT 0,
    `status` VARCHAR(20) DEFAULT 'borrowed',
    FOREIGN KEY (`book_id`) REFERENCES `books`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`member_id`) REFERENCES `members`(`id`) ON DELETE CASCADE
);
