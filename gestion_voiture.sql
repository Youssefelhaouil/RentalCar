-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : jeu. 06 juin 2024 à 01:10
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gestion_voiture`
--

-- --------------------------------------------------------

--
-- Structure de la table `administrator`
--

CREATE TABLE `administrator` (
  `admin_id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `administrator`
--

INSERT INTO `administrator` (`admin_id`, `nom`, `prenom`, `email`, `mot_de_passe`) VALUES
(1, 'efkiren', 'youssouf', 'efkiren@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `id_client` int(11) NOT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `client`
--

INSERT INTO `client` (`id_client`, `nom`, `prenom`, `email`, `mot_de_passe`) VALUES
(1, 'Doe', 'Jane', 'jane.doe@example.com', '5678'),
(2, 'Taylor', 'Liam', 'liam.taylor@example.com', '5678'),
(3, 'Wilson', 'Noah', 'noah.wilson@example.com', '5678'),
(4, 'Lee', 'Ava', 'ava.lee@example.com', '5678'),
(5, 'Walker', 'Isabella', 'isabella.walker@example.com', '5678');

-- --------------------------------------------------------

--
-- Structure de la table `manager`
--

CREATE TABLE `manager` (
  `id_manager` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `manager`
--

INSERT INTO `manager` (`id_manager`, `nom`, `prenom`, `email`, `mot_de_passe`) VALUES
(1, 'EFKIREN', 'YOUSSEF', 'EFKIREN1@gmail.com', '1234'),
(2, 'Dehri', 'redouane', 'dehri1@gmail.com', '1234'),
(3, 'Dihi', 'walid', 'dihi1@gmail.com', '1234'),
(4, 'OUALLA', 'Soufiane', 'oualla4@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Structure de la table `reservations`
--

CREATE TABLE `reservations` (
  `id_reservations` int(11) NOT NULL,
  `id_voiture` int(11) DEFAULT NULL,
  `id_client` int(11) DEFAULT NULL,
  `status` enum('pending','accepted','refused') DEFAULT 'pending',
  `refusal_message` varchar(255) DEFAULT NULL,
  `accept_message` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `voiture`
--

CREATE TABLE `voiture` (
  `id_voiture` int(11) NOT NULL,
  `marque` varchar(255) DEFAULT NULL,
  `modele` varchar(255) DEFAULT NULL,
  `immatriculation` varchar(20) DEFAULT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `disponibilite` tinyint(1) DEFAULT NULL,
  `image_data` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `voiture`
--

INSERT INTO `voiture` (`id_voiture`, `marque`, `modele`, `immatriculation`, `categorie`, `prix`, `disponibilite`, `image_data`) VALUES
(1, 'Volkswagen', 'Golf', 'M-1234-A', 'Hatchback', 300.00, 1, 'volkswagen_golf.png'),
(2, 'Volkswagen', 'Passat', 'M-5678-B', 'Sedan', 300.00, 0, 'volkswagen_passat.png'),
(3, 'Volkswagen', 'Tiguan', 'M-9101-C', 'SUV', 500.00, 1, 'volkswagen_tiguan.png'),
(4, 'Dacia', 'Logan', 'M-7890-E', 'Sedan', 250.00, 1, 'dacia_logan.png'),
(5, 'Dacia', 'Duster', 'M-1234-F', 'SUV', 250.00, 0, 'dacia_duster.png'),
(6, 'Dacia', 'Spring', 'M-9101-H', 'Electric', 250.00, 1, 'dacia_spring.png'),
(7, 'Mercedes', 'C Class', 'M-3456-J', 'Sedan', 400.00, 1, 'mercedes_cclass.png'),
(8, 'Mercedes', 'GLA', 'M-7890-K', 'SUV', 400.00, 0, 'mercedes_gla.png'),
(9, 'Mercedes', 'A Class', 'M-5678-M', 'Hatchback', 500.00, 1, 'mercedes_aclass.png');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `administrator`
--
ALTER TABLE `administrator`
  ADD PRIMARY KEY (`admin_id`);

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id_client`);

--
-- Index pour la table `manager`
--
ALTER TABLE `manager`
  ADD PRIMARY KEY (`id_manager`);

--
-- Index pour la table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id_reservations`),
  ADD KEY `id_voiture` (`id_voiture`),
  ADD KEY `id_client` (`id_client`);

--
-- Index pour la table `voiture`
--
ALTER TABLE `voiture`
  ADD PRIMARY KEY (`id_voiture`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `administrator`
--
ALTER TABLE `administrator`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `client`
--
ALTER TABLE `client`
  MODIFY `id_client` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `manager`
--
ALTER TABLE `manager`
  MODIFY `id_manager` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id_reservations` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `voiture`
--
ALTER TABLE `voiture`
  MODIFY `id_voiture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`id_voiture`) REFERENCES `voiture` (`id_voiture`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`id_client`) REFERENCES `client` (`id_client`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
