-- this script prepares a MySQL server for the AirBnB Clone V2 project
-- name of development db : hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- new user with all privileges on teh db hbnb_dev_db : hbnb_dev
-- password : hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- granting all privileges to new user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
-- granting the SELECT privilege for the user hbnb_dev in the db performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
