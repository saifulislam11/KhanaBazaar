--DROP TABLE ADMIN;

CREATE TABLE ADMIN (
	ID VARCHAR2 ( 10 ),
	LAST_NAME VARCHAR2 ( 50 ) NOT NULL,
	FIRST_NAME VARCHAR2 ( 50 ) NOT NULL,
	EMAIL VARCHAR2 ( 50 ) UNIQUE NOT NULL,
	PASSWORD_HASH VARCHAR2 ( 50 ),
	ADDRESS VARCHAR2 ( 200 ),
CONSTRAINT ADMIN_PK PRIMARY KEY ( ID ) 
);