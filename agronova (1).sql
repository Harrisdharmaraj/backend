-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 03, 2026 at 09:23 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `agronova`
--

-- --------------------------------------------------------

--
-- Table structure for table `crop`
--

CREATE TABLE `crop` (
  `id` int(11) NOT NULL,
  `user_email` varchar(120) NOT NULL,
  `crop_name` varchar(100) NOT NULL,
  `sowing_date` date NOT NULL,
  `harvest_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crop`
--

INSERT INTO `crop` (`id`, `user_email`, `crop_name`, `sowing_date`, `harvest_date`) VALUES
(1, 'suriya@gmail.com', 'Wheat', '2026-03-07', '2026-06-25'),
(2, 'agronova@gmail.com', 'cotton', '2026-03-08', '2026-08-15'),
(3, 'harishdharmarajv4241.sse@saveetha.com', 'tomato', '2026-03-09', '2026-06-07'),
(4, 'suriya@gmail.com', 'tomato', '2026-03-11', '2026-06-09'),
(5, 'ranjith@gmail.com', 'Rice', '2026-03-19', '2026-06-17'),
(6, 'suriya@gmail.com', 'lady finger', '2026-03-28', '2026-06-26'),
(7, 'suriya@gmail.com', 'rice', '2026-03-28', '2026-07-11'),
(8, 'suriya@gmail.com', 'onion ', '2026-03-28', '2026-07-11'),
(9, 'suriya@gmail.com', 'cucumber', '2026-03-28', '2026-06-26');

-- --------------------------------------------------------

--
-- Table structure for table `crop_task`
--

CREATE TABLE `crop_task` (
  `id` int(11) NOT NULL,
  `crop_id` int(11) NOT NULL,
  `task_day` int(11) NOT NULL,
  `task_date` date NOT NULL,
  `task_title` varchar(255) NOT NULL,
  `task_description` text NOT NULL,
  `is_completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crop_task`
--

INSERT INTO `crop_task` (`id`, `crop_id`, `task_day`, `task_date`, `task_title`, `task_description`, `is_completed`) VALUES
(1, 1, 1, '2026-03-08', 'Soil Prep & Sowing', 'Prepare a fine, firm seedbed. Sow certified wheat seeds at 3-5 cm depth, ensuring optimal seed-to-soil contact. Target population: 250-350 plants/m².', 1),
(2, 1, 7, '2026-03-14', 'Germination & Emergence Check', 'Monitor for seedling emergence. Ensure adequate soil moisture for uniform germination. Replant sparse areas if necessary.', 1),
(3, 1, 25, '2026-04-01', 'Tillering & N Application 1', 'When plants have 2-3 leaves, apply 1/3 of total nitrogen (e.g., 40 kg N/ha) to promote tillering. Scout for early weeds and consider herbicide application.', 1),
(4, 1, 45, '2026-04-21', 'Jointing & N Application 2', 'At the jointing stage (first node visible), apply another 1/3 of total nitrogen (e.g., 40 kg N/ha) along with phosphorus and potassium as per soil test. Monitor for pests.', 1),
(5, 1, 65, '2026-05-11', 'Booting & Critical Irrigation', 'Ensure adequate moisture during the booting stage, as this is critical for head development. Apply irrigation if rainfall is insufficient. Scout for foliar diseases and consider fungicide if risk is high.', 1),
(6, 1, 85, '2026-05-31', 'Grain Filling & Disease Scout', 'Maintain moderate soil moisture during the grain filling period. Continue monitoring for late-season diseases (e.g., rusts, fusarium head blight) and pests. Avoid water stress.', 1),
(7, 1, 105, '2026-06-20', 'Ripening & Dry Down', 'As grains reach the hard dough stage, cease irrigation to allow for natural drying down. Monitor grain moisture content for harvest readiness.', 1),
(8, 1, 110, '2026-06-25', 'Harvest', 'Harvest when grain moisture content is optimal (typically 13-15%). Use appropriate machinery to minimize grain loss.', 1),
(9, 2, 1, '2026-03-09', 'Seed Planting', 'Plant delinted cotton seeds 2-3 cm deep, 10-15 cm apart in rows 90-100 cm apart. Ensure optimal soil moisture for germination.', 1),
(11, 2, 25, '2026-04-02', 'Thinning & First Nitrogen Application', 'Thin seedlings to achieve a final plant spacing of 15-20 cm. Apply 1/3 of total nitrogen (e.g., 50 kg N/ha) as urea or similar, alongside initial weed control.', 0),
(12, 2, 50, '2026-04-27', 'Squaring & Second Nutrient Application', 'Observe first squares forming. Apply another 1/3 of total nitrogen and all phosphorus and potassium (if not applied pre-plant). Intensify pest scouting for early season pests.', 0),
(13, 2, 75, '2026-05-22', 'Peak Flowering & Bollworm Scouting', 'Cotton plants are in full bloom. Intensify scouting for bollworms (e.g., Helicoverpa armigera) and other key pests. Apply targeted insecticides if economic thresholds are met.', 0),
(14, 2, 100, '2026-06-16', 'Boll Development & Critical Irrigation', 'Bolls are rapidly developing. Ensure consistent soil moisture through irrigation, avoiding water stress which can lead to boll shedding and reduced fiber quality.', 0),
(15, 2, 130, '2026-07-16', 'Hardening Off & Potassium Boost', 'Reduce irrigation frequency to encourage boll maturation. Apply a final foliar potassium spray to aid fiber development and boll opening.', 0),
(16, 2, 150, '2026-08-05', 'Defoliation Application', 'Apply chemical defoliants (e.g., thidiazuron, tribufos) to remove leaves, allowing bolls to open uniformly and facilitating efficient mechanical harvesting.', 0),
(17, 2, 160, '2026-08-15', 'First Cotton Harvest', 'Begin harvesting when 60-70% of bolls are open. Pick clean, dry cotton, ensuring minimal trash content for optimal quality.', 0),
(20, 3, 25, '2026-04-03', 'Transplanting Seedlings', 'When seedlings have 2-3 true leaves and are 10-15 cm tall, transplant to larger pots or directly into prepared garden beds. Space plants 60-90 cm apart.', 0),
(21, 3, 35, '2026-04-13', 'First Fertilization & Staking', 'Apply a balanced liquid fertilizer (e.g., 5-10-5 NPK) at half strength. Install stakes, cages, or trellises for support as plants begin to grow vertically.', 0),
(22, 3, 45, '2026-04-23', 'Pruning & Continued Fertilization', 'Remove suckers (shoots growing in the axils of main stem and leaf branches) to encourage fruit production. Apply a balanced fertilizer again.', 0),
(23, 3, 55, '2026-05-03', 'Flowering & Fruit Set Support', 'Ensure consistent watering, especially during flowering and fruit set, to prevent blossom end rot. Monitor for pests (e.g., aphids, hornworms) and diseases (e.g., early blight).', 0),
(24, 3, 70, '2026-05-18', 'Fruit Development & Nutrient Adjustment', 'Fruits should be developing. Reduce nitrogen and increase potassium in fertilizer application to support fruit ripening. Maintain consistent soil moisture.', 0),
(25, 3, 85, '2026-06-02', 'First Harvest', 'Harvest ripe tomatoes when they are fully colored and firm. Gently twist or cut the fruit from the vine. Continue harvesting as fruits ripen.', 0),
(29, 4, 30, '2026-04-10', 'Staking/Trellising', 'Install stakes, cages, or trellises to provide support for growing plants. Gently tie main stems to the support structure as needed.', 0),
(30, 4, 45, '2026-04-25', 'Pruning & Second Fertilization', 'Prune suckers (shoots growing in leaf axils) to direct energy to fruit production. Apply a fertilizer higher in Phosphorus and Potassium (e.g., 5-10-10) to support flowering and fruit set.', 0),
(31, 4, 60, '2026-05-10', 'Pest & Disease Monitoring', 'Intensively scout for common tomato pests (e.g., aphids, hornworms) and diseases (e.g., early blight, septoria leaf spot). Apply organic or chemical controls if necessary. Ensure consistent watering to prevent stress.', 0),
(32, 4, 75, '2026-05-25', 'Third Fertilization & Fruit Development Support', 'Apply a final dose of balanced or high-K fertilizer to support fruit sizing and ripening. Maintain consistent soil moisture to prevent blossom end rot.', 0),
(33, 4, 90, '2026-06-09', 'First Harvest', 'Begin harvesting ripe tomatoes. Pick fruits when they have fully developed color and are firm to the touch. Continue harvesting every 1-3 days as fruits ripen.', 0),
(34, 5, 1, '2026-03-20', 'Seed Soaking & Nursery Prep', 'Soak rice seeds for 24 hours. Prepare a raised nursery bed, ensuring good drainage and fertility.', 0),
(35, 5, 3, '2026-03-22', 'Nursery Bed Seeding', 'Broadcast pre-germinated seeds evenly on the nursery bed. Cover lightly with soil or straw and maintain consistent moisture.', 0),
(36, 5, 15, '2026-04-03', 'Main Field Puddling & Leveling', 'Prepare the main field by puddling (wet tillage) to create a soft mud layer and level the field for uniform water distribution.', 0),
(37, 5, 20, '2026-04-08', 'Transplanting Seedlings', 'Carefully uproot 15-20 day old seedlings from the nursery and transplant them into the puddled main field, maintaining proper spacing (e.g., 20x20 cm).', 0),
(38, 5, 30, '2026-04-18', 'First Top Dressing & Weeding', 'Apply the first top dressing of nitrogen fertilizer (e.g., Urea) and perform manual or chemical weeding to control early weed growth.', 0),
(39, 5, 45, '2026-05-03', 'Second Top Dressing', 'Apply a second top dressing of balanced NPK fertilizer to support vegetative growth and panicle initiation.', 0),
(40, 5, 60, '2026-05-18', 'Panicle Initiation Stage', 'Ensure adequate water supply. Monitor for pests and diseases, applying appropriate control measures if necessary. This stage is critical for yield formation.', 0),
(41, 5, 75, '2026-06-02', 'Grain Filling Stage', 'Maintain shallow water levels. Continue monitoring for late-stage pests (e.g., rice bugs) and diseases. Ensure good nutrient availability for grain development.', 0),
(42, 5, 85, '2026-06-12', 'Drain Field', 'Drain the field completely to allow the soil to dry and facilitate uniform ripening of grains, making harvesting easier.', 0),
(43, 5, 90, '2026-06-17', 'Harvest', 'Harvest the rice crop when grains are fully mature (yellowish, hard, and moisture content around 20-25%).', 0),
(44, 6, 1, '2026-03-29', 'Soil Preparation & Sowing', 'Prepare well-drained soil, enrich with compost. Sow seeds 1 inch deep, 6-8 inches apart in rows 3 feet apart. Water thoroughly.', 0),
(45, 6, 7, '2026-04-04', 'Germination Check & Initial Watering', 'Monitor for germination. Lightly water to keep soil consistently moist, avoiding waterlogging.', 0),
(46, 6, 15, '2026-04-12', 'Thinning & First Fertilization', 'Thin seedlings to 12-18 inches apart. Apply a balanced NPK fertilizer (e.g., 10-10-10) at recommended rates around the base of plants.', 0),
(47, 6, 30, '2026-04-27', 'Second Fertilization & Weeding', 'Apply a second dose of balanced NPK fertilizer. Remove weeds manually or with shallow cultivation to reduce competition.', 0),
(48, 6, 45, '2026-05-12', 'Flowering Begins & Pest Monitoring', 'Observe for first flowers. Begin daily checks for common pests (e.g., aphids, fruit borers) and diseases. Apply organic pest control if necessary.', 0),
(49, 6, 55, '2026-05-22', 'First Harvest', 'Harvest young, tender pods (2-4 inches long) every 1-2 days using sharp shears to avoid damaging the plant.', 0),
(50, 6, 70, '2026-06-06', 'Continued Harvesting & Fertilization', 'Continue regular harvesting. Apply a liquid fertilizer rich in potassium to support continuous fruiting and plant vigor.', 0),
(51, 6, 90, '2026-06-26', 'Final Harvest & Plant Assessment', 'Perform a final harvest for the initial cycle. Assess plant health for potential extended production or prepare for crop rotation.', 0),
(52, 7, 1, '2026-03-29', 'Seed Soaking & Pre-germination', 'Soak rice seeds in water for 24 hours, then drain and incubate for 24-48 hours until sprouts appear (for nursery preparation).', 0),
(53, 7, 3, '2026-03-31', 'Nursery Bed Sowing', 'Broadcast pre-germinated seeds evenly onto a well-prepared, puddled nursery bed. Maintain shallow water level.', 0),
(54, 7, 25, '2026-04-22', 'Field Preparation & Transplanting', 'Prepare the main field by plowing, puddling, and leveling. Transplant 20-25 day old seedlings from the nursery into the main field, maintaining proper spacing.', 0),
(55, 7, 35, '2026-05-02', 'Basal Fertilizer & First Weeding', 'Apply basal NPK fertilizer (e.g., 60kg N, 30kg P2O5, 30kg K2O per hectare) and perform the first weeding to control early weed growth.', 0),
(56, 7, 50, '2026-05-17', 'Tillering Fertilizer & Second Weeding', 'Apply a top-dressing of Nitrogen fertilizer (e.g., 30kg N per hectare) to promote tillering. Conduct the second weeding.', 0),
(57, 7, 70, '2026-06-06', 'Panicle Initiation Fertilizer', 'Apply the final top-dressing of Nitrogen and Potassium fertilizer (e.g., 30kg N, 30kg K2O per hectare) at the panicle initiation stage to support grain development.', 0),
(58, 7, 85, '2026-06-21', 'Pest & Disease Scouting', 'Regularly scout for common rice pests (e.g., stem borers, leaf folders) and diseases (e.g., blast, bacterial blight). Apply appropriate control measures if thresholds are met.', 0),
(59, 7, 95, '2026-07-01', 'Field Draining', 'Drain the field completely to allow the grains to ripen uniformly and facilitate harvesting. This typically occurs 10-15 days before harvest.', 0),
(60, 7, 105, '2026-07-11', 'Harvesting', 'Harvest the rice crop when 80-85% of the grains are golden yellow and hard. This can be done manually or mechanically.', 0),
(61, 8, 1, '2026-03-29', 'Soil Preparation & Planting', 'Prepare a well-drained bed with compost. Plant onion seeds 1/2 inch deep or sets 1 inch deep, 4-6 inches apart in rows. Water thoroughly.', 0),
(62, 8, 10, '2026-04-07', 'Germination Check & Initial Weeding', 'Monitor for seedling emergence (if direct seeding). Carefully remove any weeds to reduce competition for nutrients and light.', 0),
(63, 8, 25, '2026-04-22', 'First Thinning & Nitrogen Side-dressing', 'Thin seedlings to 4-6 inches apart. Apply a nitrogen-rich fertilizer (e.g., 20g Urea per 10L water) as a side-dressing to promote leaf growth.', 0),
(64, 8, 45, '2026-05-12', 'Second Weeding & Balanced Fertilizer Application', 'Perform a thorough weeding. Apply a balanced NPK fertilizer (e.g., 15-15-15 at 30g per 10L water) to support overall plant development and early bulb formation.', 0),
(65, 8, 65, '2026-06-01', 'Pest/Disease Scouting & Moisture Management', 'Inspect plants for common pests (thrips, onion maggot) or diseases (downy mildew). Maintain consistent soil moisture, especially crucial during bulb enlargement.', 0),
(66, 8, 85, '2026-06-21', 'Reduce Watering for Maturation', 'As onion tops begin to soften and fall over, gradually reduce watering to encourage bulb maturation and improve storage quality.', 0),
(67, 8, 105, '2026-07-11', 'Harvest', 'Harvest when 70-80% of the tops have fallen over and turned yellow. Loosen soil around bulbs and gently pull them from the ground.', 0),
(68, 8, 106, '2026-07-12', 'Curing', 'Lay harvested onions in a warm, dry, well-ventilated area for 2-3 weeks to cure. This dries the neck and outer skins, preparing them for long-term storage.', 0),
(69, 9, 1, '2026-03-29', 'Seed Sowing', 'Direct sow cucumber seeds 1 inch deep and 3-5 inches apart in well-drained soil, or start indoors in peat pots. Ensure soil temperature is above 60°F (15°C). Water thoroughly after planting.', 0),
(70, 9, 7, '2026-04-04', 'Germination Check & Initial Watering', 'Monitor for seedling emergence. Keep soil consistently moist but not waterlogged. Lightly water if the top inch of soil feels dry.', 0),
(71, 9, 14, '2026-04-11', 'Thinning / Transplanting', 'If direct sown, thin seedlings to 12-18 inches apart, selecting the strongest plants. If started indoors, transplant seedlings to their final outdoor location, ensuring minimal root disturbance.', 0),
(72, 9, 21, '2026-04-18', 'First Balanced Fertilizer Application', 'Apply a balanced liquid fertilizer (e.g., 5-10-5 or 10-10-10) at half strength, or a granular slow-release fertilizer around the base of the plants. Water well after application.', 0),
(73, 9, 30, '2026-04-27', 'Trellising / Support System Installation', 'Install a trellis, cage, or stakes for vining varieties to climb. This improves air circulation, reduces disease risk, and keeps fruit clean. Gently guide vines onto the support.', 0),
(74, 9, 40, '2026-05-07', 'Pest & Disease Scouting / Prevention', 'Regularly inspect plants for signs of pests (aphids, cucumber beetles) or diseases (powdery mildew, downy mildew). Apply organic pest control or fungicides as needed. Ensure good air circulation.', 0),
(75, 9, 50, '2026-05-17', 'Second Fertilizer Application (Flowering Support)', 'Apply a fertilizer higher in potassium and phosphorus (e.g., 5-10-10 or a \'bloom\' formula) to support flowering and fruit development. Avoid excessive nitrogen at this stage.', 0),
(76, 9, 60, '2026-05-27', 'First Harvest', 'Begin harvesting cucumbers when they reach desired size and are firm. Harvest frequently (every 1-2 days) to encourage continuous production. Use a sharp knife or pruners to cut the stem.', 0),
(77, 9, 75, '2026-06-11', 'Pruning & Ongoing Maintenance', 'Remove any yellowing, diseased, or damaged leaves. Prune back excessive foliage to improve light penetration and air flow. Continue regular watering and monitor for pests.', 0),
(78, 9, 90, '2026-06-26', 'Continuous Harvest & Nutrient Replenishment', 'Maintain consistent harvesting. Apply a light side-dressing of compost or a balanced liquid fertilizer every 2-3 weeks to sustain plant vigor and fruit production throughout the season.', 0);

-- --------------------------------------------------------

--
-- Table structure for table `resource`
--

CREATE TABLE `resource` (
  `id` int(11) NOT NULL,
  `user_email` varchar(120) NOT NULL,
  `owner_name` varchar(100) NOT NULL,
  `owner_phone` varchar(15) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `category` varchar(50) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `resource`
--

INSERT INTO `resource` (`id`, `user_email`, `owner_name`, `owner_phone`, `item_name`, `category`, `latitude`, `longitude`, `is_available`, `created_at`) VALUES
(1, 'suriya@gmail.com', 'Suriya', 'Not Provided', 'Tractor', 'Transport', 12.8302, 79.7138, 1, '2026-03-07 17:24:12'),
(5, 'harishdharmarajv4241.sse@saveetha.com', 'harish', 'Not Provided', 'Seeds', 'Seeds/Fertilizer', 13.0242, 80.0157, 1, '2026-03-10 13:28:41'),
(6, 'suriya@gmail.com', 'Suriya', 'Not Provided', 'blades ', 'Machinery', 12.8302, 79.7138, 1, '2026-03-11 14:00:48'),
(8, 'nithi@gmail.com', 'Nithi', '9876456321', 'Seeds', 'Seeds', 13.024, 80.0159, 1, '2026-03-19 16:20:00'),
(9, 'suriya@gmail.com', 'Suriya', 'Not Provided', 'Bag seeds', 'Seeds/Fertilizer', 13.0265, 80.016, 1, '2026-03-30 12:21:29');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `location_string` varchar(255) DEFAULT NULL,
  `preferred_language` varchar(50) DEFAULT 'English'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `username`, `email`, `phone`, `password_hash`, `profile_photo`, `latitude`, `longitude`, `location_string`, `preferred_language`) VALUES
(1, 'Ranjith r', NULL, 'ranjith@gmail.com', '3636363636', 'scrypt:32768:8:1$QDURB6jeiNyi7N7y$57f96e0ccc715915a95ee2b298c741098fe0b654fb4380a1260a6453957c324f6231253ed31225600ec1559d62a31adbfa2b8b36a83eb1c4e0fa236b8ffccfc7', NULL, NULL, NULL, NULL, 'English'),
(2, 'ranji', NULL, 's@gmail.com', '1234567890', 'scrypt:32768:8:1$gLb1UtQNWShEgZRb$0d509bfe00f2291b1edc91ddbd721b1e9b79421ce2e25143dcee8f3cd146eed216fc779e6d889b1fb9e41b5ce90c0a4fc19d493649932300275a96b84c20b31d', NULL, NULL, NULL, NULL, 'English'),
(3, 'Suriya', 'Suriya@9', 'suriya@gmail.com', '5656565656', 'scrypt:32768:8:1$oYQ1hpQwwWzfZ7M5$822507c0d2930f974de6797ed68ad7eec6b8cb1d61ce208584d6b338085d0417e45bada8faf493ac06097fcfd793d7ea5e453f65858acafea59eb86b180a450f', 'C:\\Users\\velu9\\OneDrive\\Desktop\\AgroNova_Backend\\uploads\\profile_3_2699a8d7.jpg', 13.0265, 80.016, 'Kuthambakkam, Tamil Nadu', 'English'),
(4, 'Agronova', NULL, 'agronova@gmail.com', '9966996699', 'scrypt:32768:8:1$GIL57kSp779rZDpi$92f547202bb410cd64892258947e97a07cdeaefc0c636aeeacf7e12e6bc1077c8ecfe854a9c1f359c1e9401b85623e4075fcea498d40e2a4540413b7283566e6', NULL, 12.8303, 79.7138, 'Kanchipuram, Tamil Nadu', 'English'),
(5, 'harish', 'harish@604', 'harishdharmarajv4241.sse@saveetha.com', '6363636363', 'scrypt:32768:8:1$S8oftVhL4CJnP9Gp$0e584375e41d2961564857c7c1a36e07a670560006759f4748c9948933d49fbbf661aacbcfdeb18e13da2235005f770eba16610dad92940d6e3565a9166d6e80', 'C:\\Users\\velu9\\OneDrive\\Desktop\\AgroNova_Backend\\uploads\\profile_5_3e1cba42.jpg', 13.0242, 80.0157, 'Chennai, Tamil Nadu', 'English'),
(6, 'Nithi', NULL, 'nithi@gmail.com', '9876456321', 'scrypt:32768:8:1$g48FHc2bqxIOk4mO$8c1aa643980c342e21d36cd87a6d395ff83508ed620c9451be78153f433e3dd84e77099577ac79bbc0d842716a29f0af694049b5529c4db929de109184df31ee', NULL, 13.0242, 80.0156, 'Chennai, Tamil Nadu', 'English');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crop`
--
ALTER TABLE `crop`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `crop_task`
--
ALTER TABLE `crop_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `crop_id` (`crop_id`);

--
-- Indexes for table `resource`
--
ALTER TABLE `resource`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crop`
--
ALTER TABLE `crop`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `crop_task`
--
ALTER TABLE `crop_task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `resource`
--
ALTER TABLE `resource`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `crop_task`
--
ALTER TABLE `crop_task`
  ADD CONSTRAINT `crop_task_ibfk_1` FOREIGN KEY (`crop_id`) REFERENCES `crop` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
