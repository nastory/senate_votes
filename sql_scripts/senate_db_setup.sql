USE senate;

DROP TABLE IF EXISTS proceedings;
CREATE TABLE IF NOT EXISTS proceedings
(
	`congress` INT,
    `year` INT,
    `vote_number` VARCHAR(5),
    `session` INT,
    `vote_date` DATETIME,
    `issue` VARCHAR(50),
    `question` VARCHAR(255),
    `title` TEXT,
    `yeas` INT,
    `nays` INT,
    `result` VARCHAR(25),
    PRIMARY KEY (`congress`, `year`, `vote_number`)
);

DROP TABLE IF EXISTS votes;
CREATE TABLE IF NOT EXISTS votes
(
	`congress` INT,
    `year` INT,
    `vote_number` VARCHAR(5),
    `senator_id` INT,
    `vote` VARCHAR(25),
    PRIMARY KEY (`congress`, `year`, `vote_number`, `senator_id`)
);

DROP TABLE IF EXISTS senators;
CREATE TABLE IF NOT EXISTS senators
(
	`senator_id` INT,
    `name` VARCHAR(255),
    `state` VARCHAR(5),
    `district` VARCHAR(255),
    `party` VARCHAR(255),
    PRIMARY KEY (`senator_id`)
);
