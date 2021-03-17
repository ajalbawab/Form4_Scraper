-- --------------------------------------------------------
-- Host:                         Station26
-- Server version:               10.5.7-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for form4db
CREATE DATABASE IF NOT EXISTS `form4db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `form4db`;

-- Dumping structure for table form4db.form4
CREATE TABLE IF NOT EXISTS `form4` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Issuer` varchar(50) DEFAULT NULL,
  `CIKNumber` varchar(50) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  KEY `Index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4168 DEFAULT CHARSET=latin1;

-- Dumping data for table form4db.form4: ~0 rows (approximately)
/*!40000 ALTER TABLE `form4` DISABLE KEYS */;
/*!40000 ALTER TABLE `form4` ENABLE KEYS */;

-- Dumping structure for table form4db.scrapeddata
CREATE TABLE IF NOT EXISTS `scrapeddata` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CIKNumber` varchar(50) DEFAULT NULL,
  `DateofEvent` date DEFAULT NULL,
  `TransactionType` varchar(50) DEFAULT NULL,
  `FullName` varchar(50) DEFAULT NULL,
  `ownerCIK` varchar(50) DEFAULT NULL,
  `secName` varchar(255) DEFAULT NULL,
  `numberowned` double DEFAULT NULL,
  `numbertrans` double DEFAULT NULL,
  `percentChange` double DEFAULT NULL,
  `ownerdesc` varchar(255) DEFAULT NULL,
  `issuer` varchar(50) DEFAULT NULL,
  KEY `INDEX` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5476 DEFAULT CHARSET=latin1;

-- Dumping data for table form4db.scrapeddata: ~0 rows (approximately)
/*!40000 ALTER TABLE `scrapeddata` DISABLE KEYS */;
/*!40000 ALTER TABLE `scrapeddata` ENABLE KEYS */;

-- Dumping structure for table form4db.uniquedata
CREATE TABLE IF NOT EXISTS `uniquedata` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CIKNumber` varchar(50) DEFAULT NULL,
  `DateofEvent` date DEFAULT NULL,
  `TransactionType` varchar(50) DEFAULT NULL,
  `FullName` varchar(50) DEFAULT NULL,
  `ownerCIK` varchar(50) DEFAULT NULL,
  `secName` varchar(255) DEFAULT NULL,
  `numberowned` double DEFAULT NULL,
  `numbertrans` double DEFAULT NULL,
  `percentChange` double DEFAULT NULL,
  KEY `Index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=898 DEFAULT CHARSET=latin1;

-- Dumping data for table form4db.uniquedata: ~0 rows (approximately)
/*!40000 ALTER TABLE `uniquedata` DISABLE KEYS */;
/*!40000 ALTER TABLE `uniquedata` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
