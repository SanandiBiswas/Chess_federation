-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: chess_federation
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `disputes`
--

DROP TABLE IF EXISTS `disputes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disputes` (
  `dispute_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int DEFAULT NULL,
  `official_id` int DEFAULT NULL,
  `type` enum('Eligibility','Election','Tournament','Finance') DEFAULT NULL,
  `description` text,
  `status` enum('Pending','Resolved','Court') DEFAULT 'Pending',
  `resolution_date` date DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  PRIMARY KEY (`dispute_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disputes`
--

LOCK TABLES `disputes` WRITE;
/*!40000 ALTER TABLE `disputes` DISABLE KEYS */;
INSERT INTO `disputes` VALUES (1,103,104,'Eligibility','Rash Behavior to another player','Pending','2026-01-24','2026-01-09'),(2,103,104,'Eligibility','Cheating in game','Pending','2026-02-01','2026-01-17'),(3,103,104,'Eligibility','Use of Foreign Object to calculate moves','Pending','2026-02-01','2026-01-17');
/*!40000 ALTER TABLE `disputes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finances`
--

DROP TABLE IF EXISTS `finances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finances` (
  `trans_id` int NOT NULL AUTO_INCREMENT,
  `tournament_id` int DEFAULT NULL,
  `player_id` int DEFAULT NULL,
  `trans_date` date DEFAULT NULL,
  `admin_fee` decimal(10,2) NOT NULL DEFAULT '200.00',
  `price` decimal(10,2) NOT NULL DEFAULT '800.00',
  `entryfee` decimal(10,2) NOT NULL DEFAULT '1000.00',
  PRIMARY KEY (`trans_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finances`
--

LOCK TABLES `finances` WRITE;
/*!40000 ALTER TABLE `finances` DISABLE KEYS */;
INSERT INTO `finances` VALUES (1,1001,101,'2026-01-17',300.00,1200.00,1500.00),(2,1002,104,'2026-01-17',400.00,1600.00,2000.00);
/*!40000 ALTER TABLE `finances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `Uname` varchar(50) NOT NULL,
  `Passwd` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Uname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES ('admin','admin');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officials`
--

DROP TABLE IF EXISTS `officials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `officials` (
  `official_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `role` enum('President','Secretary','Treasurer','Arbiter','Committee') DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(70) DEFAULT NULL,
  `term_start` date DEFAULT NULL,
  `term_end` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`official_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officials`
--

LOCK TABLES `officials` WRITE;
/*!40000 ALTER TABLE `officials` DISABLE KEYS */;
INSERT INTO `officials` VALUES (101,'Jane Smith','President','0987654321','president@fed.com','2025-12-19','2029-12-19',1),(102,'Bob Wilson','Arbiter','1122334455','arbiter@fed.com','2025-12-19','2029-12-19',1),(103,'Aryan Singh','Secretary','1234567890','secretary@fed.com','2025-01-19','2029-01-19',1),(104,'Sania Mishra','Arbiter','1237890456','sania@fed.com','2021-01-09','2025-01-09',0),(105,'Alex Bonapart','Committee','7890123456','alex@fed.com','2026-01-17','2030-01-17',1);
/*!40000 ALTER TABLE `officials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `age_category` enum('U8','U10','U12','U14','U16','U18','U20','Senior') DEFAULT NULL,
  `fide_rating` int DEFAULT '1000',
  `phone` bigint DEFAULT NULL,
  `email` varchar(70) DEFAULT NULL,
  `membership_status` enum('Active','Inactive','Suspended') DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (101,'John Doe','2009-12-05','U16',1250,1234567890,'john@fed.com','Active','2025-12-19'),(102,'Alice Johnson','2008-03-20','U18',2700,9087654321,'alicetu@fed.com','Active','2025-12-19'),(103,'Harsh Mishra','1980-01-22','Senior',2203,4560123789,'harsh@fed.com','Suspended','2000-02-12'),(104,'Ram Singh','2008-05-15','U18',2601,1045692378,'ram@fed.com','Active','2026-01-17');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tournaments`
--

DROP TABLE IF EXISTS `tournaments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tournaments` (
  `tournament_id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `format` enum('Swiss','Round Robin') DEFAULT 'Swiss',
  `entry_fee` decimal(10,2) NOT NULL DEFAULT '1000.00',
  `total_prize` decimal(10,2) NOT NULL DEFAULT '800.00',
  `status` enum('Upcoming','Ongoing','Completed') DEFAULT 'Ongoing',
  `age_category` enum('Open') NOT NULL DEFAULT 'Open',
  PRIMARY KEY (`tournament_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournaments`
--

LOCK TABLES `tournaments` WRITE;
/*!40000 ALTER TABLE `tournaments` DISABLE KEYS */;
INSERT INTO `tournaments` VALUES (1001,'John Doe','2026-01-17','2026-02-06','Swiss',1500.00,1200.00,'Ongoing','Open'),(1002,'Ram Singh','2026-01-17','2026-02-06','Swiss',2000.00,1600.00,'Ongoing','Open');
/*!40000 ALTER TABLE `tournaments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-23 21:54:36
