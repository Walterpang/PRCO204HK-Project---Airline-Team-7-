CREATE TABLE `airline`.`tbl_user` (
  `user_id` BIGINT AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
  `user_password` VARCHAR(45) NULL,
  `user_email` VARCHAR(45) NULL,
  `user_confirm` Boolean  default '0',
  PRIMARY KEY (`user_id`));
  
  