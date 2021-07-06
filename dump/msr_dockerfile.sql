-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 06, 2021 alle 20:34
-- Versione del server: 10.4.17-MariaDB
-- Versione PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `msr_dockerfile`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `languages`
--

CREATE TABLE `languages` (
  `id_language` int(50) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `id_repository` int(50) NOT NULL,
  `percentage` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `repositories`
--

CREATE TABLE `repositories` (
  `id_repository` int(50) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `github_url` varchar(500) CHARACTER SET utf8 NOT NULL,
  `n_stars` int(50) NOT NULL,
  `dockerfile_instructions` int(50) NOT NULL,
  `n_contributors` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struttura della tabella `smells`
--

CREATE TABLE `smells` (
  `id_smell` int(50) NOT NULL,
  `category` varchar(50) CHARACTER SET utf8 NOT NULL,
  `description` varchar(500) CHARACTER SET utf8 NOT NULL,
  `type` varchar(50) CHARACTER SET utf8 NOT NULL,
  `repository_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `languages`
--
ALTER TABLE `languages`
  ADD PRIMARY KEY (`id_language`),
  ADD KEY `id_repository` (`id_repository`);

--
-- Indici per le tabelle `repositories`
--
ALTER TABLE `repositories`
  ADD PRIMARY KEY (`id_repository`);

--
-- Indici per le tabelle `smells`
--
ALTER TABLE `smells`
  ADD PRIMARY KEY (`id_smell`),
  ADD KEY `repository_id` (`repository_id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `languages`
--
ALTER TABLE `languages`
  MODIFY `id_language` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `repositories`
--
ALTER TABLE `repositories`
  MODIFY `id_repository` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `smells`
--
ALTER TABLE `smells`
  MODIFY `id_smell` int(50) NOT NULL AUTO_INCREMENT;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `languages`
--
ALTER TABLE `languages`
  ADD CONSTRAINT `languages_ibfk_1` FOREIGN KEY (`id_repository`) REFERENCES `repositories` (`id_repository`);

--
-- Limiti per la tabella `smells`
--
ALTER TABLE `smells`
  ADD CONSTRAINT `smells_ibfk_1` FOREIGN KEY (`repository_id`) REFERENCES `repositories` (`id_repository`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
