--db생성 관련 스크립트
-- 확인하고 변경하여 사용할 것!

-- grant all privileges on mydb.* to myuser @ %;
-- grant all privileges on mydb.* to 'myuser' @'%'; /터미널에선 % 가려줘야함
use mydb;
create table UserInfo(
    -- ID INT AUTO_INCREMENT integer primary key,
    name varchar(50) NOT NULL,
    UserId varchar(50) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    Email varchar(255) UNIQUE NOT NULL,
    -- price integer 추후 추가
);

-- show databases;
-----------------------------------------------------------

--  CREATE DATABASE WeatherDB;
grant all privileges on WeatherDB.* to 'myuser'@'%';
USE WeatherDB;

CREATE TABLE weatherData6 (
    
    PRIMARY KEY (tm,stnId), -- 지점과 시간 조합을 기본키로 설정  
    tm DATETIME NOT NULL,  
    wtId VARCHAR(10) NOT NULL,
    wt char(20) NOT NULL
);

grant all privileges on WeatherDB.* to 
FLUSH PRIVILEGES;


CREATE USER 'myuser'@'%' IDENTIFIED BY '0000';
grant all privileges on WeatherDB.* to 'myuser'@'%';
GRANT SELECT ON mysql.user TO 'myuser'@'%';
FLUSH PRIVILEGES;
SELECT * FROM mysql.user WHERE User;a

show columns from weatherData6;
SELECT * FROM weatherData6;

drop DATABASE WeatherData6;