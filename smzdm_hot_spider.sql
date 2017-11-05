-- phpMyAdmin SQL Dump
-- version 4.7.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2017-11-05 14:32:07
-- 服务器版本： 5.7.20
-- PHP Version: 5.6.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smzdm`
--

-- --------------------------------------------------------

--
-- 表的结构 `smzdm_record`
--

CREATE TABLE `smzdm_hot_record` (
  `id` int(11) NOT NULL,
  `price` varchar(1000) DEFAULT NULL,
  `page_url` varchar(1000) DEFAULT NULL,
  `md5` varchar(255) NOT NULL,
  `title` varchar(1000) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `smzdm_record`
--
ALTER TABLE `smzdm_hot_record`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `smzdm_hot_record_id_uindex` (`id`),
  ADD KEY `md5_index` (`md5`) USING BTREE;

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `smzdm_record`
--
ALTER TABLE `smzdm_hot_record`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
