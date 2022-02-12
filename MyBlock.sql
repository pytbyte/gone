-- MySQL dump 10.17  Distrib 10.3.15-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: MyBlock
-- ------------------------------------------------------
-- Server version	10.3.15-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bids`
--

DROP TABLE IF EXISTS `bids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `origin` varchar(200) NOT NULL,
  `budget` varchar(200) NOT NULL,
  `quantity` varchar(200) NOT NULL,
  `details` varchar(400) NOT NULL,
  `requesttime` varchar(200) NOT NULL,
  `request_views` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  `destination` varchar(200) DEFAULT NULL,
  `author_id` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bids`
--

LOCK TABLES `bids` WRITE;
/*!40000 ALTER TABLE `bids` DISABLE KEYS */;
INSERT INTO `bids` VALUES (1,'rider','50','0','','','0','0','zuri Towers','James '),(2,'rider','50','0','two passangers','','0','0','zuri Towers','James '),(3,'rider','300','0','two passangers','','0','0','zuri Towers','James '),(4,'rider','300','0','two passangers','','0','0','zuri Towers','James '),(5,'rider','300','0','two passangers','','0','0','zuri Towers','24'),(6,'rider','500','2','transport for two ','','0','0','Thiririka','24'),(7,'rider','50','1','Ride for two','','0','0','Noon Booth','24'),(8,'rider','50','1','trial','','0','0','Town','24'),(9,'rider','50','1','hurry home','Tue, 01 Feb 2022 19:00:49 GMT','0','0','Maragua','24'),(10,'taxi','50','1','payload','Tue, 01 Feb 2022 19:00:49 GMT','0','0','trial','24'),(11,'truck','50','1','going somewhere','Tue, 01 Feb 2022 19:00:49 GMT','0','0','ruai','24'),(12,'rider','700','1','transport for 2.','Wed, 02 Feb 2022 13:07:40 GMT','0','0','Githurai','25'),(13,'rider','400','1','swift ride , i passanger','Wed, 02 Feb 2022 13:07:40 GMT','0','0','Drop zone ent','25'),(14,'rider','50','1','500mbs','Sat, 12 Feb 2022 10:52:31 GMT','0','0','majengo','24');
/*!40000 ALTER TABLE `bids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bikes`
--

DROP TABLE IF EXISTS `bikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bikes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_no` varchar(200) NOT NULL,
  `contact` varchar(200) NOT NULL,
  `make` varchar(200) NOT NULL,
  `route` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  `last_seen` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `registered_on` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bikes`
--

LOCK TABLES `bikes` WRITE;
/*!40000 ALTER TABLE `bikes` DISABLE KEYS */;
INSERT INTO `bikes` VALUES (5,'kmfb 669r','0701977677','super Dayun','ndarasha','Patrick','Sat, 29 Jan 2022 17:21:17 GMT','0','Sat, 29 Jan 2022 17:21:17 GMT',NULL),(6,'kmfq 123d','0701977677','bugati','ndarasha','Patrick','Sat, 29 Jan 2022 17:28:27 GMT','0','Sat, 29 Jan 2022 17:28:27 GMT',NULL),(7,'kmfg 200k','0724731639','ranger','kingston','James ','Sun, 30 Jan 2022 16:26:01 GMT','0','Sun, 30 Jan 2022 16:26:01 GMT',NULL),(8,'kmf9 200k','0724731639','ranger','kingston','James ','Sun, 30 Jan 2022 16:30:11 GMT','0','Sun, 30 Jan 2022 16:30:11 GMT',NULL),(9,'kmf9h 200k','0724731639','ranger','kingston','James ','Sun, 30 Jan 2022 16:33:50 GMT','0','Sun, 30 Jan 2022 16:33:50 GMT',NULL),(10,'kmh 200k','0724731639','ranger','kingston','James ','Sun, 30 Jan 2022 16:44:09 GMT','0','Sun, 30 Jan 2022 16:44:09 GMT',NULL),(11,'kmnh','0724731639','njui','de','James ','Sun, 30 Jan 2022 16:54:26 GMT','0','Sun, 30 Jan 2022 16:54:26 GMT',NULL),(12,'kmnn','0724731639','njui','de','James ','Sun, 30 Jan 2022 16:56:14 GMT','0','Sun, 30 Jan 2022 16:56:14 GMT',NULL),(13,'kmno','0724731639','njui','de','James ','Sun, 30 Jan 2022 16:57:43 GMT','0','Sun, 30 Jan 2022 16:57:43 GMT',NULL),(14,'kmnog','0724731639','njui','de','James ','Sun, 30 Jan 2022 17:03:27 GMT','0','Sun, 30 Jan 2022 17:03:27 GMT',NULL),(15,'ksda','0719168752','suzuki','45','pytbyte','Mon, 31 Jan 2022 10:44:41 GMT','0','Mon, 31 Jan 2022 10:44:41 GMT','static/images/bikes/15/12daab10-095b-4680-9f21-e863ec4ade9c.jpg'),(16,'kmfr 400l','0719168752','suzuki','Mastore','pytbyte','Mon, 31 Jan 2022 10:46:20 GMT','0','Mon, 31 Jan 2022 10:46:20 GMT',NULL),(17,'kmfy 400l','0719168752','suzuki','Mastore','pytbyte','Mon, 31 Jan 2022 10:53:04 GMT','0','Mon, 31 Jan 2022 10:53:04 GMT',NULL),(18,'kmfm 400l','0719168752','suzuki','Mastore','pytbyte','Mon, 31 Jan 2022 10:54:04 GMT','0','Mon, 31 Jan 2022 10:54:04 GMT',NULL),(19,'kmdd 345','0719168752','kingsy','red','pytbyte','Mon, 31 Jan 2022 11:45:19 GMT','0','Mon, 31 Jan 2022 11:45:19 GMT',NULL),(20,'kmd 345','0719168752','kingsy','red','pytbyte','Mon, 31 Jan 2022 11:54:50 GMT','0','Mon, 31 Jan 2022 11:54:50 GMT',NULL),(21,'kmfr 567','0719168752','jingchen','45','pytbyte','Mon, 31 Jan 2022 11:59:24 GMT','0','Mon, 31 Jan 2022 11:59:24 GMT',NULL),(22,'kmfo 567','0719168752','jingchen','45','pytbyte','Mon, 31 Jan 2022 12:03:36 GMT','0','Mon, 31 Jan 2022 12:03:36 GMT',NULL),(23,'kmfg 440l','0719168752','dayun','kisii','pytbyte','Mon, 31 Jan 2022 12:24:40 GMT','0','Mon, 31 Jan 2022 12:24:40 GMT',NULL),(24,'kfmg 300n','0719168752','jingcheng','dcii','pytbyte','Mon, 31 Jan 2022 12:26:26 GMT','0','Mon, 31 Jan 2022 12:26:26 GMT',NULL),(25,'gmn 99','0719168752','iokk','bb','pytbyte','Mon, 31 Jan 2022 12:31:29 GMT','0','Mon, 31 Jan 2022 12:31:29 GMT',NULL);
/*!40000 ALTER TABLE `bikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business`
--

DROP TABLE IF EXISTS `business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `businessname` varchar(200) DEFAULT NULL,
  `businesscontact` varchar(200) DEFAULT NULL,
  `authenticated` tinyint(1) DEFAULT NULL,
  `businesscategory` varchar(200) DEFAULT NULL,
  `businesslocation` varchar(200) DEFAULT NULL,
  `registered_on` varchar(200) DEFAULT NULL,
  `last_seen` varchar(200) DEFAULT NULL,
  `owner` varchar(200) DEFAULT NULL,
  `logo_url` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `businessdsc` varchar(500) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  `currency` varchar(300) DEFAULT NULL,
  `workinghours` varchar(200) DEFAULT NULL,
  `latlng` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `businessname` (`businessname`),
  UNIQUE KEY `businesscontact` (`businesscontact`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business`
--

LOCK TABLES `business` WRITE;
/*!40000 ALTER TABLE `business` DISABLE KEYS */;
INSERT INTO `business` VALUES (51,'Pytlabs','0701977677',0,'Software',NULL,'Tue, 04 Jan 2022 20:58:18 GMT','Tue, 04 Jan 2022 20:58:18 GMT','Patrick',NULL,0,'creating futuristic solutions with python',NULL,NULL,'24/7',NULL),(57,'fashion ke','0701900000',0,'fashion',NULL,'Tue, 04 Jan 2022 21:35:25 GMT','Tue, 04 Jan 2022 21:35:25 GMT','Patrick',NULL,0,'alot of staff',NULL,NULL,'24/7',NULL),(58,'zippys Salon','07210778995',0,'beauty',NULL,'Fri, 07 Jan 2022 14:39:01 GMT','Fri, 07 Jan 2022 14:39:01 GMT','Patrick',NULL,0,'fresh',NULL,NULL,'24/7',''),(59,'top tops','0700334998',0,'Fashion',NULL,'Sun, 09 Jan 2022 12:24:25 GMT','Sun, 09 Jan 2022 12:24:25 GMT','Patrick',NULL,0,'fashion trend',NULL,NULL,'3-3',''),(60,'yuris','070033400',0,'Fashion',NULL,'Sun, 09 Jan 2022 13:50:52 GMT','Sun, 09 Jan 2022 13:50:52 GMT','Patrick',NULL,0,'fashion trend',NULL,NULL,'3-3','');
/*!40000 ALTER TABLE `business` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `item_name` varchar(45) NOT NULL,
  `author_id` varchar(45) NOT NULL,
  `quantity` varchar(200) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `Total` varchar(200) DEFAULT NULL,
  `item_cost` varchar(200) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (54,117,'Malenge','39','1',NULL,'10','10','Fri, 07 May 2021 21:19:34 GMT','static/media/business/products/39/745508a6-b18e-4c54-a6f4-96bad9ed5a97.jpg'),(57,116,'Dresses','39','1',NULL,'2500','2500','Fri, 07 May 2021 21:34:24 GMT','static/media/business/products/39/c95fbd79-0249-41e1-a4a8-955f38d587b3.jpg'),(58,118,'Business Account','39','1',NULL,'100','100','Sat, 08 May 2021 17:55:50 GMT','static/media/business/products/39/63bb8677-5203-47cf-8fab-64a20389356d.jpg?name=orig'),(59,112,'Urban shoes','39','1',NULL,'350','350','Sun, 09 May 2021 19:08:58 GMT','static/media/business/products/7/6aea6e9e-6dcd-4871-a482-07f169547e4e.jpg'),(60,119,'Boots','39','1',NULL,'4500','4500','Sun, 09 May 2021 19:08:58 GMT','static/media/business/products/39/103da382-ff7b-4dfc-9e50-c6c619a11745.jpg'),(61,120,'Sneakers','39','1',NULL,'3000','3000','Sun, 09 May 2021 19:08:58 GMT','static/media/business/products/39/8aaf1d9b-d5f4-4be8-bcf4-738611560c0f.jpg'),(113,129,'Old School','9','1',NULL,'2000000','2000000','Tue, 13 Jul 2021 22:14:12 GMT','static/media/business/products/39/4aa88886-043d-4109-98b8-d3d036c3616b.jpg'),(114,125,'Wedge','9','1',NULL,'1700','1700','Tue, 13 Jul 2021 22:14:12 GMT','static/media/business/products/39/04468e52-86de-476f-9d0f-38f149feb062.jpg'),(115,133,'zanzibar getaway','11','1',NULL,'5600','5600','Sat, 17 Jul 2021 20:46:04 GMT','static/media/business/products/40/1bdcf28e-edcd-4f91-9288-a8f1a49e3c5a.png'),(116,132,'TRACK PARTY','13','1',NULL,'2000','2000','Wed, 21 Jul 2021 14:31:44 GMT','static/media/business/products/40/7b40ccb6-edd7-4d20-b439-e34ac9fca31d.jpg'),(117,134,'test1','11','1',NULL,'6000','6000','Thu, 22 Jul 2021 04:56:03 GMT','static/media/business/products/43/affe624d-1ae1-45b7-8353-a1eac90980d0.jpg');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` varchar(200) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `service_body` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `product_id` (`product_id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_title` varchar(200) DEFAULT NULL,
  `event_venue` varchar(200) DEFAULT NULL,
  `event_date` varchar(200) DEFAULT NULL,
  `event_time` varchar(200) DEFAULT NULL,
  `event_description` varchar(200) DEFAULT NULL,
  `event_category` varchar(200) DEFAULT NULL,
  `price` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `author_id` varchar(200) DEFAULT NULL,
  `share` varchar(200) DEFAULT NULL,
  `event_views` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `image_url1` varchar(200) DEFAULT NULL,
  `image_url2` varchar(200) DEFAULT NULL,
  `image_url3` varchar(200) DEFAULT NULL,
  `image_url4` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow_ups`
--

DROP TABLE IF EXISTS `follow_ups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow_ups` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follow_ups_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `follow_ups_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow_ups`
--

LOCK TABLES `follow_ups` WRITE;
/*!40000 ALTER TABLE `follow_ups` DISABLE KEYS */;
/*!40000 ALTER TABLE `follow_ups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interests`
--

DROP TABLE IF EXISTS `interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `interest_` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  CONSTRAINT `interests_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interests`
--

LOCK TABLES `interests` WRITE;
/*!40000 ALTER TABLE `interests` DISABLE KEYS */;
/*!40000 ALTER TABLE `interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` int(11) DEFAULT NULL,
  `recipient` int(11) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `content` varchar(2000) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sender` (`sender`),
  KEY `recipient` (`recipient`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender`) REFERENCES `users` (`id`),
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`recipient`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity` varchar(200) DEFAULT NULL,
  `notified_user` varchar(200) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `author` varchar(200) DEFAULT NULL,
  `message` varchar(400) DEFAULT NULL,
  `data_url` varchar(200) DEFAULT NULL,
  `user_data_url` varchar(200) DEFAULT NULL,
  `status_code` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_notifications_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_title` varchar(200) DEFAULT NULL,
  `product_category` varchar(200) DEFAULT NULL,
  `price` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `share` int(11) DEFAULT NULL,
  `views` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `image_url1` varchar(200) DEFAULT NULL,
  `image_url2` varchar(200) DEFAULT NULL,
  `image_url3` varchar(200) DEFAULT NULL,
  `image_url4` varchar(200) DEFAULT NULL,
  `product_description` varchar(600) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (137,NULL,'uioo',NULL,0,'Tue, 08 Feb 2022 11:43:47 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'guigiuig'),(138,'0rion','hao',NULL,0,'Tue, 08 Feb 2022 12:19:05 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'wateja'),(139,'d','d','2',0,'Tue, 08 Feb 2022 12:19:05 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'dd'),(140,'fesh','vegies','56',0,'Tue, 08 Feb 2022 13:15:33 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'t'),(141,'UI','home','90',0,'Tue, 08 Feb 2022 13:46:03 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'JJJJH'),(142,'UIn','home','90',0,'Tue, 08 Feb 2022 13:46:03 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'JJJJH'),(143,'UInss','home','90',0,'Tue, 08 Feb 2022 13:46:03 GMT',51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'JJJJH');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_title` varchar(200) DEFAULT NULL,
  `service_description` varchar(200) DEFAULT NULL,
  `service_category` varchar(200) DEFAULT NULL,
  `price` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `timestamp` varchar(200) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `share` int(11) DEFAULT NULL,
  `service_views` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `image_url1` varchar(200) DEFAULT NULL,
  `image_url2` varchar(200) DEFAULT NULL,
  `image_url3` varchar(200) DEFAULT NULL,
  `image_url4` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `share`
--

DROP TABLE IF EXISTS `share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `share` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `share`
--

LOCK TABLES `share` WRITE;
/*!40000 ALTER TABLE `share` DISABLE KEYS */;
/*!40000 ALTER TABLE `share` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taxis`
--

DROP TABLE IF EXISTS `taxis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taxis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_no` varchar(200) NOT NULL,
  `contact` varchar(200) NOT NULL,
  `make` varchar(200) NOT NULL,
  `route` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  `last_seen` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `registered_on` varchar(200) DEFAULT NULL,
  `seater` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taxis`
--

LOCK TABLES `taxis` WRITE;
/*!40000 ALTER TABLE `taxis` DISABLE KEYS */;
INSERT INTO `taxis` VALUES (1,'KDG 4550','0719168752','Range','KARIOBANGI','pytbyte','Tue, 01 Feb 2022 04:04:29 GMT','0','Tue, 01 Feb 2022 04:04:29 GMT','','static/images/taxis/1/eb3b630b-01be-4dc4-baef-9834da12bedd.jpg'),(2,'KDS 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:09:23 GMT','0','Tue, 01 Feb 2022 04:09:23 GMT','7',NULL),(3,'KDt 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:10:53 GMT','0','Tue, 01 Feb 2022 04:10:53 GMT','7',NULL),(4,'KDA 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:14:18 GMT','0','Tue, 01 Feb 2022 04:14:18 GMT','7',NULL),(5,'KDK 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:19:07 GMT','0','Tue, 01 Feb 2022 04:19:07 GMT','7',NULL),(6,'KDM 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:36:29 GMT','0','Tue, 01 Feb 2022 04:36:29 GMT','7',NULL),(7,'KDDD 445E','0719168752','Premio','Juja','pytbyte','Tue, 01 Feb 2022 04:37:43 GMT','0','Tue, 01 Feb 2022 04:37:43 GMT','7',NULL),(8,'KDH 300P','0719168752','VITZ','KARIOBANGI','pytbyte','Tue, 01 Feb 2022 04:51:06 GMT','0','Tue, 01 Feb 2022 04:51:06 GMT','5',NULL);
/*!40000 ALTER TABLE `taxis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trucks`
--

DROP TABLE IF EXISTS `trucks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trucks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_no` varchar(200) NOT NULL,
  `contact` varchar(200) NOT NULL,
  `make` varchar(200) NOT NULL,
  `route` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  `last_seen` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `registered_on` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trucks`
--

LOCK TABLES `trucks` WRITE;
/*!40000 ALTER TABLE `trucks` DISABLE KEYS */;
INSERT INTO `trucks` VALUES (1,'KGH 500M','0719168752','','Dandora','pytbyte','Tue, 01 Feb 2022 05:48:11 GMT','static/images/trucks/1/71fa0d41-528e-4f3c-b000-05e53a79be20.jpg','0','Tue, 01 Feb 2022 05:48:11 GMT'),(2,'KGS 400N','0719168752','ISUZU','yesa','pytbyte','Tue, 01 Feb 2022 05:51:08 GMT',NULL,'0','Tue, 01 Feb 2022 05:51:08 GMT'),(3,'KGN 400N','0719168752','ISUZU','yesa','pytbyte','Tue, 01 Feb 2022 05:55:22 GMT',NULL,'0','Tue, 01 Feb 2022 05:55:22 GMT'),(4,'KGN 488Z','0719168752','ISUZU','yesa','pytbyte','Tue, 01 Feb 2022 05:57:09 GMT',NULL,'0','Tue, 01 Feb 2022 05:57:09 GMT'),(5,'KMFS 544l','0719168752','Datsun','Thika','pytbyte','Tue, 01 Feb 2022 05:59:44 GMT',NULL,'0','Tue, 01 Feb 2022 05:59:44 GMT'),(6,'KMFS 540l','0719168752','Datsun','Thika','pytbyte','Tue, 01 Feb 2022 06:08:04 GMT',NULL,'0','Tue, 01 Feb 2022 06:08:04 GMT'),(7,'KMFS 547l','0719168752','Datsun','Thika','pytbyte','Tue, 01 Feb 2022 06:10:23 GMT',NULL,'0','Tue, 01 Feb 2022 06:10:23 GMT'),(8,'nht 677m','0719168752','budi','rty','pytbyte','Tue, 01 Feb 2022 06:26:30 GMT',NULL,'0','Tue, 01 Feb 2022 06:26:30 GMT');
/*!40000 ALTER TABLE `trucks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `authenticated` tinyint(1) DEFAULT NULL,
  `password_hash` varchar(200) DEFAULT NULL,
  `registered_on` varchar(200) DEFAULT NULL,
  `last_seen` varchar(200) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `latlon` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact` (`contact`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (22,'Patrick','zabby@aqua.com','0701977677',0,'pbkdf2:sha256:150000$O5QXnEVm$3c6003d08acada16e3bc5a2b99e6779386f719ac4632c671fabf2d8f8135f762','Thu, 02 Dec 2021 18:40:29 GMT','Sat, 12 Feb 2022 11:03:09 GMT','static/images/personal/profile/22/a1a80e8f-c18c-49aa-874a-0114e2d8da35.jpg',0,NULL),(23,'pytbyte','hapakusoma@gmail.com','0719168752',0,'pbkdf2:sha256:150000$bv6eHAhh$d860f6ab9f410d5e76d7f38610955e01387cfb9095d76db82f710f0a7948cb7e','Sat, 29 Jan 2022 11:18:07 GMT','Fri, 04 Feb 2022 13:12:14 GMT','static/images/personal/profile/23/ad61f647-d5ee-4230-bfdf-c83df844d6c8.jpg',0,NULL),(24,'James ','james1@gmail.com','0724731639',0,'pbkdf2:sha256:150000$OPA4qdxL$71ba21f296c62163f59581267a10087058e7061c02cae7efbfa5bdd53fe050e0','Sun, 30 Jan 2022 12:49:14 GMT','Sat, 12 Feb 2022 12:03:20 GMT','static/images/personal/profile/24/897e8307-2749-4101-91cb-f2a8ebc130ae.jpg',0,NULL),(25,'Dommie Macharia','dommie@gmail.com','0745223224',0,'pbkdf2:sha256:150000$CHGRyMij$fbfb3d418aeb6c2b32dffa792df0d3fa1aa840ba59431d7482cbbffa3861ce5c','Wed, 02 Feb 2022 13:13:37 GMT','Wed, 02 Feb 2022 22:51:59 GMT','static/images/personal/profile/25/a7e2c351-ecf2-40e3-8461-524f2bca57ad.jpg',0,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-12 13:28:14
