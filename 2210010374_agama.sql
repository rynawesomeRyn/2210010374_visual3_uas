-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2025 at 08:02 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2210010017_agama`
--

-- --------------------------------------------------------

--
-- Table structure for table `acara_keagamaan`
--

CREATE TABLE `acara_keagamaan` (
  `id_acara` int(11) NOT NULL,
  `nama_acara` varchar(100) NOT NULL,
  `tanggal_acara` date NOT NULL,
  `lokasi` varchar(100) NOT NULL,
  `deskripsi` varchar(255) NOT NULL,
  `dibuat_oleh` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `acara_keagamaan`
--

INSERT INTO `acara_keagamaan` (`id_acara`, `nama_acara`, `tanggal_acara`, `lokasi`, `deskripsi`, `dibuat_oleh`) VALUES
(3112, 'Syukuran', '2025-02-02', 'Masjid', 'Syukuran 30 hari', 'Riduan'),
(3113, 'Aqiqah', '2025-03-03', 'Rumah', 'Aqiqah Syifa', 'Syifa');

-- --------------------------------------------------------

--
-- Table structure for table `kamera`
--

CREATE TABLE `kamera` (
  `id_kamera` int(11) NOT NULL,
  `nama_kamera` varchar(50) NOT NULL,
  `lokasi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kamera`
--

INSERT INTO `kamera` (`id_kamera`, `nama_kamera`, `lokasi`) VALUES
(4122, 'Sonia', 'Adiyaksa'),
(4123, 'Nokia', 'Sungai Andai');

-- --------------------------------------------------------

--
-- Table structure for table `masjid`
--

CREATE TABLE `masjid` (
  `id_masjid` int(11) NOT NULL,
  `nama_masjid` varchar(100) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `lokasi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `masjid`
--

INSERT INTO `masjid` (`id_masjid`, `nama_masjid`, `alamat`, `lokasi`) VALUES
(23445, 'Ar Rahman', 'Sultan Adam', 'Pinggir Jalan'),
(23446, 'As Syifa', 'Kayu Tangi', 'Komplek');

-- --------------------------------------------------------

--
-- Table structure for table `pengunjung_masjid`
--

CREATE TABLE `pengunjung_masjid` (
  `id_pengunjung` int(11) NOT NULL,
  `nama_pengunjung` varchar(50) NOT NULL,
  `jenis_kelamin` enum('Laki-laki','Perempuan') NOT NULL,
  `tanggal_kunjungan` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pengunjung_masjid`
--

INSERT INTO `pengunjung_masjid` (`id_pengunjung`, `nama_pengunjung`, `jenis_kelamin`, `tanggal_kunjungan`) VALUES
(6778, 'Riduan', 'Laki-laki', '2025-12-12'),
(6779, 'Mega', 'Perempuan', '2025-05-05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acara_keagamaan`
--
ALTER TABLE `acara_keagamaan`
  ADD PRIMARY KEY (`id_acara`);

--
-- Indexes for table `kamera`
--
ALTER TABLE `kamera`
  ADD PRIMARY KEY (`id_kamera`);

--
-- Indexes for table `masjid`
--
ALTER TABLE `masjid`
  ADD PRIMARY KEY (`id_masjid`);

--
-- Indexes for table `pengunjung_masjid`
--
ALTER TABLE `pengunjung_masjid`
  ADD PRIMARY KEY (`id_pengunjung`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kamera`
--
ALTER TABLE `kamera`
  MODIFY `id_kamera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41257;

--
-- AUTO_INCREMENT for table `masjid`
--
ALTER TABLE `masjid`
  MODIFY `id_masjid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23447;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
