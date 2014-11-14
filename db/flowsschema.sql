-- MySQL dump 10.13  Distrib 5.1.67, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: flows
-- ------------------------------------------------------
-- Server version	5.1.67

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `GRAPH`
--

DROP TABLE IF EXISTS `GRAPH`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GRAPH` (
  `gid` int(11) NOT NULL AUTO_INCREMENT,
  `graph_name` varchar(100) DEFAULT NULL,
  `graph_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`gid`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `JOB`
--

DROP TABLE IF EXISTS `JOB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `JOB` (
  `jid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL DEFAULT '0',
  `stime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`jid`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NET2NET`
--

DROP TABLE IF EXISTS `NET2NET`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NET2NET` (
  `nn_id` int(11) NOT NULL AUTO_INCREMENT,
  `fn_id` int(11) NOT NULL DEFAULT '0',
  `tn_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`nn_id`),
  UNIQUE KEY `fn_id` (`fn_id`,`tn_id`)
) ENGINE=MyISAM AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NETWORK`
--

DROP TABLE IF EXISTS `NETWORK`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NETWORK` (
  `n_id` int(11) NOT NULL AUTO_INCREMENT,
  `tom` set('interface','as','network') NOT NULL DEFAULT '',
  `asn` int(11) DEFAULT NULL,
  `interface` int(11) DEFAULT NULL,
  `label` varchar(20) NOT NULL DEFAULT '',
  `min_byte_flow` int(11) DEFAULT NULL,
  `max_byte_flow` int(11) DEFAULT NULL,
  PRIMARY KEY (`n_id`),
  UNIQUE KEY `label` (`label`),
  UNIQUE KEY `interface` (`interface`),
  UNIQUE KEY `asn` (`asn`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NET_BLOCK`
--

DROP TABLE IF EXISTS `NET_BLOCK`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NET_BLOCK` (
  `nb_id` int(11) NOT NULL AUTO_INCREMENT,
  `n_id` int(11) NOT NULL DEFAULT '0',
  `ip_from` int(11) unsigned NOT NULL DEFAULT '0',
  `ip_to` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`nb_id`),
  UNIQUE KEY `ip_from` (`ip_from`,`ip_to`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PORT`
--

DROP TABLE IF EXISTS `PORT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PORT` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `n_id` int(11) NOT NULL DEFAULT '0',
  `port` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`p_id`),
  UNIQUE KEY `n_id` (`n_id`,`port`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SESION`
--

DROP TABLE IF EXISTS `SESION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SESION` (
  `sid` varchar(30) NOT NULL DEFAULT '',
  `uid` int(11) NOT NULL DEFAULT '0',
  `lasttime` varchar(20) NOT NULL DEFAULT '',
  `remote_addr` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `USUARIO`
--

DROP TABLE IF EXISTS `USUARIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USUARIO` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL DEFAULT '',
  `passwd` varbinary(100) DEFAULT NULL,
  `phone` varchar(15) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `staff` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `USUARIO_NETWORK`
--

DROP TABLE IF EXISTS `USUARIO_NETWORK`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USUARIO_NETWORK` (
  `unid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL DEFAULT '0',
  `n_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`unid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `USUARIO_VIEW`
--

DROP TABLE IF EXISTS `USUARIO_VIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USUARIO_VIEW` (
  `v_id` int(11) DEFAULT NULL,
  `u_id` int(11) DEFAULT NULL,
  KEY `v_id` (`v_id`),
  KEY `u_id` (`u_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `VIEW`
--

DROP TABLE IF EXISTS `VIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VIEW` (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `view_name` varchar(100) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`vid`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `VIEW_GRAPH`
--

DROP TABLE IF EXISTS `VIEW_GRAPH`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VIEW_GRAPH` (
  `v_id` int(11) DEFAULT NULL,
  `g_id` int(11) DEFAULT NULL,
  KEY `v_id` (`v_id`),
  KEY `g_id` (`g_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iptocountry`
--

DROP TABLE IF EXISTS `iptocountry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iptocountry` (
  `ip_from` int(11) unsigned DEFAULT NULL,
  `ip_to` int(11) unsigned DEFAULT NULL,
  `registry` varchar(10) DEFAULT NULL,
  `fecha` int(11) unsigned DEFAULT NULL,
  `country_code2` char(2) DEFAULT NULL,
  `country_code3` char(3) DEFAULT NULL,
  `country_name` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rrd_n`
--

DROP TABLE IF EXISTS `rrd_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rrd_n` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nid` int(11) NOT NULL,
  `ioctect` int(10) unsigned NOT NULL,
  `ooctect` int(10) unsigned NOT NULL,
  `ipacks` int(10) unsigned NOT NULL,
  `opacks` int(10) unsigned NOT NULL,
  `iflows` int(10) unsigned NOT NULL,
  `oflows` int(10) unsigned NOT NULL,
  `time_unix` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nid_time_unix` (`nid`,`time_unix`)
) ENGINE=MyISAM AUTO_INCREMENT=2060527 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rrd_port`
--

DROP TABLE IF EXISTS `rrd_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rrd_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `ioctect` int(10) unsigned NOT NULL,
  `ooctect` int(10) unsigned NOT NULL,
  `ipacks` int(10) unsigned NOT NULL,
  `opacks` int(10) unsigned NOT NULL,
  `iflows` int(10) unsigned NOT NULL,
  `oflows` int(10) unsigned NOT NULL,
  `time_unix` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=974038 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rrd_port_backup`
--

DROP TABLE IF EXISTS `rrd_port_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rrd_port_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `ooctect` int(10) unsigned NOT NULL,
  `ioctect` int(10) unsigned NOT NULL,
  `ipacks` int(10) unsigned NOT NULL,
  `opacks` int(10) unsigned NOT NULL,
  `oflows` int(10) unsigned NOT NULL,
  `iflows` int(10) unsigned NOT NULL,
  `time` text NOT NULL,
  `time_unix` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=308141 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rrd_to_net`
--

DROP TABLE IF EXISTS `rrd_to_net`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rrd_to_net` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ioctect` int(10) unsigned NOT NULL,
  `ooctect` int(10) unsigned NOT NULL,
  `ipacks` int(10) unsigned NOT NULL,
  `opacks` int(10) unsigned NOT NULL,
  `iflows` int(10) unsigned NOT NULL,
  `oflows` int(10) unsigned NOT NULL,
  `nn_id` int(11) NOT NULL,
  `time_unix` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3030340 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rrd_to_net_backup`
--

DROP TABLE IF EXISTS `rrd_to_net_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rrd_to_net_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ooctect` int(10) unsigned NOT NULL,
  `ioctect` int(10) unsigned NOT NULL,
  `opacks` int(10) unsigned NOT NULL,
  `ipacks` int(10) unsigned NOT NULL,
  `oflows` int(10) unsigned NOT NULL,
  `iflows` int(10) unsigned NOT NULL,
  `time` text NOT NULL,
  `nn_id` int(11) NOT NULL,
  `time_unix` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=339269 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-12-16 16:14:01
