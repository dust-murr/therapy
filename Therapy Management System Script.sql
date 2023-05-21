-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema therapy_management_system
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `therapy_management_system` ;

-- -----------------------------------------------------
-- Schema therapy_management_system
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `therapy_management_system` DEFAULT CHARACTER SET latin1 ;
USE `therapy_management_system` ;

-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_group` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_group` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`django_content_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`django_content_type` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`django_content_type` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label` ASC, `model` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_permission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_permission` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_permission` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `content_type_id` INT(11) NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id` ASC, `codename` ASC),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `therapy_management_system`.`django_content_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 41
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_group_permissions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_group_permissions` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_group_permissions` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `group_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id` ASC, `permission_id` ASC),
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id` ASC),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `therapy_management_system`.`auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `therapy_management_system`.`auth_group` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_user` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME(6) NULL DEFAULT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_user_groups`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_user_groups` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_user_groups` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `group_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id` ASC, `group_id` ASC),
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id` ASC),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `therapy_management_system`.`auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `therapy_management_system`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`auth_user_user_permissions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`auth_user_user_permissions` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`auth_user_user_permissions` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id` ASC, `permission_id` ASC),
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id` ASC),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `therapy_management_system`.`auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `therapy_management_system`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`django_admin_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`django_admin_log` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`django_admin_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `action_time` DATETIME(6) NOT NULL,
  `object_id` LONGTEXT NULL DEFAULT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT(5) UNSIGNED NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id` ASC),
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id` ASC),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `therapy_management_system`.`django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `therapy_management_system`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`django_migrations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`django_migrations` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`django_migrations` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 37
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`django_session`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`django_session` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  INDEX `django_session_expire_date_a5c62663` (`expire_date` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`therapy_appointment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`therapy_appointment` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`therapy_appointment` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `patientName` VARCHAR(100) NULL DEFAULT NULL,
  `therapistName` VARCHAR(100) NULL DEFAULT NULL,
  `appointmentDate` DATETIME(6) NOT NULL,
  `status` TINYINT(1) NOT NULL,
  `patient_id` INT(10) UNSIGNED NULL DEFAULT NULL,
  `therapist_id` INT(10) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`therapy_discharge`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`therapy_discharge` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`therapy_discharge` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `patientName` VARCHAR(100) NOT NULL,
  `assignedTherapistName` VARCHAR(100) NULL DEFAULT NULL,
  `address` VARCHAR(100) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  `symptoms` VARCHAR(100) NULL DEFAULT NULL,
  `registerDate` DATETIME(6) NOT NULL,
  `lastVisitDate` DATETIME(6) NOT NULL,
  `visitNumber` INT(10) UNSIGNED NOT NULL,
  `copay` INT(10) UNSIGNED NOT NULL,
  `treatmentCost` INT(10) UNSIGNED NOT NULL,
  `therapistFee` INT(10) UNSIGNED NOT NULL,
  `otherCharge` INT(10) UNSIGNED NOT NULL,
  `total` INT(10) UNSIGNED NOT NULL,
  `patient_id` INT(10) UNSIGNED NULL DEFAULT NULL,
  `status` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`therapy_patient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`therapy_patient` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`therapy_patient` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(50) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  `symptoms` VARCHAR(100) NOT NULL,
  `registerDate` DATETIME(6) NOT NULL,
  `status` TINYINT(1) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `assignedTherapist` INT(10) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id` ASC),
  CONSTRAINT `therapy_patient_user_id_a31cd754_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `therapy_management_system`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `therapy_management_system`.`therapy_therapist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `therapy_management_system`.`therapy_therapist` ;

CREATE TABLE IF NOT EXISTS `therapy_management_system`.`therapy_therapist` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `department` VARCHAR(50) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  `status` TINYINT(1) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id` ASC),
  CONSTRAINT `therapy_therapist_user_id_6d615a00_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `therapy_management_system`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
