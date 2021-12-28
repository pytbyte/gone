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
  `author` varchar(200) NOT NULL,
  `budget` varchar(200) NOT NULL,
  `quantity` varchar(200) NOT NULL,
  `details` varchar(400) NOT NULL,
  `requesttime` varchar(200) NOT NULL,
  `request_views` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bids`
--

LOCK TABLES `bids` WRITE;
/*!40000 ALTER TABLE `bids` DISABLE KEYS */;
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
  `image_url` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bikes`
--

LOCK TABLES `bikes` WRITE;
/*!40000 ALTER TABLE `bikes` DISABLE KEYS */;
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
  `businessemail` varchar(200) NOT NULL,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `businessemail` (`businessemail`),
  UNIQUE KEY `businessname` (`businessname`),
  UNIQUE KEY `businesscontact` (`businesscontact`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business`
--

LOCK TABLES `business` WRITE;
/*!40000 ALTER TABLE `business` DISABLE KEYS */;
INSERT INTO `business` VALUES (39,'Zenge Technologies Ltd','heretolearn3@gmail.com','0701977678',0,'Fashion','Eldoret','Thu, 15 Apr 2021 00:11:50 GMT','Thu, 22 Jul 2021 07:17:44 GMT','Paulo',NULL,0,'The number one payment facilitator',1,'USD'),(40,'Alemar Adventures','kiemo@gmail.com','0720114282',0,'Tourism','Nairobi','Thu, 15 Jul 2021 12:48:23 GMT','Thu, 22 Jul 2021 07:14:44 GMT','Kiemo','static/media/business/logo/40/88402cf4-4f44-4f2e-ac2e-587f5b59a65a.jpg',0,'Travel Agency\r\n0720114282\r\n0721204120\r\n0736000955\r\n',1,'KSH'),(48,'koko fuel','koko@gmail.com','0701988766',0,'Home and Living','Kiambu','Wed, 21 Jul 2021 12:43:43 GMT','Wed, 21 Jul 2021 13:58:38 GMT','Zab','static/media/business/logo/48/1b9720ac-efa3-4e4a-8359-75427405b8d3.jpg',0,'Koko sales and refiels.',1,'KSH');
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
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (119,'Boots','Fashion','4500',1,'Thu, 03 Jun 2021 11:53:54 GMT',39,NULL,NULL,'static/media/business/products/39/103da382-ff7b-4dfc-9e50-c6c619a11745.jpg','static/media/business/products/39/6fb3f596-76fa-452a-955e-dad0b3d648ed.jpg','static/media/business/products/39/2568b3de-aae7-4d68-a51b-e4108c44ea4c.jpg','static/media/business/products/39/c55af211-abbe-4af1-8bbd-4d3490e0cf9e.jpg',NULL,'Quality Boots '),(120,'Sneakers','Fashion','3000',1,'Tue, 15 Jun 2021 09:34:53 GMT',39,NULL,NULL,'static/media/business/products/39/8aaf1d9b-d5f4-4be8-bcf4-738611560c0f.jpg','static/media/business/products/39/81b513c3-8897-4087-a368-a36052f2585d.jpg','static/media/business/products/39/0e90b752-3a95-44bc-9f32-5259754cfdcf.jpg',NULL,NULL,'cool Sneakers'),(121,'LandRover Defenders','Cars','1200000',1,'Tue, 08 Jun 2021 23:14:02 GMT',39,NULL,NULL,'static/media/business/products/39/3376bebf-af29-4646-9978-cf87f7a12835.jpg','static/media/business/products/39/f60d9088-fc3f-46df-9e7f-b58b562d9125.jpg','static/media/business/products/39/36c19be8-620a-4685-a4ec-07d0855cb549.jpg',NULL,NULL,'Quality Pimp for that country road or City stroll.\r\n\r\nSame old Power drive both manual and auto.\r\nService and Maintenance provides free for 1 year.\r\nPrice: ksh 1.2M'),(122,'alot','Fashion','7000',1,'Thu, 03 Jun 2021 11:53:54 GMT',39,NULL,NULL,'static/media/business/products/39/7c7c6752-cd35-423f-ac4f-655d684d07e2.jpg','static/media/business/products/39/ec02458f-75b9-4828-974e-d14646ae72fb.jpg','static/media/business/products/39/25e5872d-0257-4aba-af75-e7521f721ee2.jpg','static/media/business/products/39/d8189606-4887-418a-8060-75702668770c.jpg',NULL,'Original and reliable staff'),(123,'LandRover Defenders','Cars','5000000',1,'Thu, 03 Jun 2021 11:53:54 GMT',39,NULL,NULL,'static/media/business/products/39/ae2fde9f-e1a8-40dd-832a-a0fcf7ba151d.jpg','static/media/business/products/39/72697608-8fe2-46cf-a21c-216142e32ef9.jpg','static/media/business/products/39/83f5502c-28a0-4eac-9a5d-c0b0d698d727.jpg','static/media/business/products/39/1cd9cf33-8e3a-47b7-9075-4e9525b6f6fd.jpg',NULL,'Tough new cars'),(124,'jmat','Fashion','4500',1,'Sat, 05 Jun 2021 15:03:03 GMT',39,NULL,NULL,'static/media/business/products/39/167c5f4a-a5c9-49ac-8c4b-bff2847bfd79.jpg','static/media/business/products/39/87e969f8-6555-409f-90df-3cd5d79bb6cc.jpg','static/media/business/products/39/9f7e668c-81db-4627-99c0-6c565964fb82.jpg','static/media/business/products/39/9dae73db-de44-4089-b6de-272a7e489e63.jpg',NULL,'mats'),(125,'Wedge','Fashion','1700',1,'Mon, 05 Jul 2021 16:51:02 GMT',39,NULL,NULL,'static/media/business/products/39/04468e52-86de-476f-9d0f-38f149feb062.jpg','static/media/business/products/39/c1ef0fb8-f848-479c-9312-a78c4d693a91.jpg','static/media/business/products/39/becde8c8-d8de-4125-953b-ce61031e250f.jpg','static/media/business/products/39/0291d475-1b00-43f3-b578-f6a8255d072c.jpg','static/media/business/products/39/89be920a-4dd4-4ba5-b12c-e12a017d8b88.jpg','Classy light Leather wedge shoes.'),(126,'Classic Official ','Fashion','2000',1,'Mon, 05 Jul 2021 16:51:02 GMT',39,NULL,NULL,'static/media/business/products/39/2b6a2811-4ae3-4a90-a77e-00a3b6df2cb1.jpg','static/media/business/products/39/9f61bd0f-e55c-4014-ab81-ba14cf85df9e.jpg','static/media/business/products/39/e2eea861-8996-488c-ac19-7d78c5386aa0.jpg','static/media/business/products/39/5c6be531-a6d5-42e1-b6ca-b18502976d56.jpg','static/media/business/products/39/b3b9f999-bf60-4f36-8d81-e4edeb98e04e.jpg','Good long lasting quality. what you see is what you get.'),(127,'Boots','Fashion','2500',1,'Mon, 05 Jul 2021 16:51:02 GMT',39,NULL,NULL,'static/media/business/products/39/d47e9932-6bff-4089-b281-0696aaf8123b.jpg','static/media/business/products/39/88dc5953-9d96-4eef-a5bb-6f392629262d.jpg','static/media/business/products/39/ac3d5270-6dc8-416f-b972-9019a52b1907.jpg','static/media/business/products/39/521d677e-145f-4eb9-bf71-0d1becb15f05.jpg',NULL,'Warm boots'),(128,'Rides','Cars','1000000',1,'Mon, 05 Jul 2021 16:51:02 GMT',39,NULL,NULL,'static/media/business/products/39/879e25c7-706f-48c7-91d9-84b2606494eb.jpg','static/media/business/products/39/1148b482-784b-47d7-8fe5-12724c77eec4.jpg','static/media/business/products/39/edcac4ab-ed53-4142-ba6f-5c83493d9c7e.jpg',NULL,NULL,'Any deal for 1m .'),(129,'Old School','Cars','2000000',1,'Mon, 05 Jul 2021 16:51:02 GMT',39,NULL,NULL,'static/media/business/products/39/4aa88886-043d-4109-98b8-d3d036c3616b.jpg','static/media/business/products/39/ea460990-519a-457b-ada0-2297cab84c88.jpg','static/media/business/products/39/ba9a7c5d-7582-4b55-b000-dd7c14f9bc09.jpg',NULL,NULL,'Pimped old school cars.'),(130,'bedsheets','Fashion','6',1,'Thu, 15 Jul 2021 08:24:22 GMT',39,NULL,NULL,'static/media/business/products/39/d413f54f-b436-4dd2-b44a-66d7feda577f.jpg',NULL,NULL,NULL,NULL,'100% COTTON'),(131,'samburu roadtrip','Choose...','3500',1,'Thu, 15 Jul 2021 14:17:45 GMT',40,NULL,NULL,'static/media/business/products/40/557d9744-61f8-460a-9610-f9c6579c1976.jpg',NULL,NULL,NULL,NULL,'track party'),(132,'TRACK PARTY','Choose...','2000',0,'Thu, 15 Jul 2021 14:17:45 GMT',40,NULL,NULL,'static/media/business/products/40/7b40ccb6-edd7-4d20-b439-e34ac9fca31d.jpg','static/media/business/products/40/398f53bc-6c67-47f3-904c-247199daeb7c.jpg',NULL,NULL,NULL,'Samburu Track Party'),(133,'zanzibar getaway','Cars','5600',0,'Sun, 18 Jul 2021 14:34:40 GMT',40,NULL,NULL,'static/media/business/products/40/1bdcf28e-edcd-4f91-9288-a8f1a49e3c5a.png','static/media/business/products/40/7dc64a2b-7b4f-4d2f-bca8-98c2ff1707a8.png',NULL,NULL,NULL,'5 days zanzibar getaway '),(134,'test1','Fashion','6000',0,'Wed, 21 Jul 2021 14:31:44 GMT',48,NULL,NULL,'static/media/business/products/43/affe624d-1ae1-45b7-8353-a1eac90980d0.jpg','static/media/business/products/43/fe5d9d20-0cb5-4e98-91a6-9facee828737.jpg','static/media/business/products/43/58426644-5a41-4836-99d9-719b44a9200f.jpg','static/media/business/products/43/9416f8c3-052c-4760-8f36-27e10e8106f8.jpg','static/media/business/products/43/e746d49b-325d-4cfd-891c-464b7b67a682.jpg','some test data'),(135,'Safari Truck','Cars','3000000',0,'Thu, 22 Jul 2021 04:56:03 GMT',40,NULL,NULL,'static/media/business/products/40/120491a3-fb52-4f13-8d51-ff8b4e336d7a.jpg',NULL,NULL,NULL,NULL,'NEW fully equipped Safari Truck.');
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
  `seaters` varchar(200) NOT NULL,
  `route` varchar(200) NOT NULL,
  `image_url` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taxis`
--

LOCK TABLES `taxis` WRITE;
/*!40000 ALTER TABLE `taxis` DISABLE KEYS */;
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
  `weight` varchar(200) NOT NULL,
  `route` varchar(200) NOT NULL,
  `image_url` varchar(200) NOT NULL,
  `owner` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trucks`
--

LOCK TABLES `trucks` WRITE;
/*!40000 ALTER TABLE `trucks` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (22,'Patrick','zabby@aqua.com','0701977677',0,'pbkdf2:sha256:150000$O5QXnEVm$3c6003d08acada16e3bc5a2b99e6779386f719ac4632c671fabf2d8f8135f762','Thu, 02 Dec 2021 18:40:29 GMT','Sun, 26 Dec 2021 20:44:31 GMT','static/images/personal/profile/22/a1a80e8f-c18c-49aa-874a-0114e2d8da35.jpg',0,NULL);
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

-- Dump completed on 2021-12-27 14:36:33
