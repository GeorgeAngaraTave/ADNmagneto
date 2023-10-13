-- --------------------------------------------------------
-- Host:                         34.122.218.102
-- Versión del servidor:         5.7.33-google-log - (Google)
-- SO del servidor:              Linux
-- HeidiSQL Versión:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para proyectos
CREATE DATABASE IF NOT EXISTS `proyectos` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `proyectos`;

-- Volcando estructura para tabla proyectos.adns
CREATE TABLE IF NOT EXISTS `adns` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sequence` varchar(100) DEFAULT NULL,
  `is_valid` tinyint(4) DEFAULT '0',
  `added_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_on` timestamp NULL DEFAULT NULL,
  KEY `Índice 1` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla proyectos.adns: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `adns` DISABLE KEYS */;
INSERT INTO `adns` (`id`, `sequence`, `is_valid`, `added_on`, `update_on`) VALUES
	(1, '[\'ATGCGA\', \'CAGTGC\', \'TTATGT\', \'AGAAGG\', \'CCCCTA\', \'TCACTG\']', 1, '2021-06-09 03:40:08', NULL),
	(2, '[\'ATGCGA\', \'CAGTGC\', \'TTATTT\', \'AGACGG\', \'GCGTCA\', \'TCACTG\']', 0, '2021-06-09 03:40:57', NULL),
	(3, '[\'ATGCGA\', \'CAGTGC\', \'TTATGT\', \'GATTCC\', \'AAAACT\', \'TCACTG\']', 1, '2021-06-09 03:45:52', NULL);
/*!40000 ALTER TABLE `adns` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
