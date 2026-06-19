-- Stock Analyzer MySQL Database Schema Setup
-- To import this schema into your MySQL server, run:
-- mysql -u your_username -p < schema.sql

CREATE DATABASE IF NOT EXISTS `stock_analyzer` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `stock_analyzer`;

-- --------------------------------------------------------
-- Table Structure for `users`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `cash_balance` DECIMAL(15, 2) NOT NULL DEFAULT 100000.00,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table Structure for `holdings`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `holdings` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `ticker` VARCHAR(10) NOT NULL,
  `shares` DECIMAL(15, 4) NOT NULL DEFAULT 0.0000,
  `average_price` DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
  UNIQUE KEY `_user_ticker_uc` (`user_id`, `ticker`),
  CONSTRAINT `fk_holdings_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table Structure for `transactions`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `transactions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `ticker` VARCHAR(10) NOT NULL,
  `action` VARCHAR(10) NOT NULL, -- 'BUY' or 'SELL'
  `shares` DECIMAL(15, 4) NOT NULL,
  `price` DECIMAL(15, 2) NOT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_transactions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
