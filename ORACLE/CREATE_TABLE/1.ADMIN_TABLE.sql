CREATE TABLE ADMIN (
	ID CHAR ( 10 ),
	LAST_NAME VARCHAR2 ( 50 ) NOT NULL,
	FIRST_NAME VARCHAR2 ( 50 ) NOT NULL,
	EMAIL VARCHAR2 ( 50 ) UNIQUE NOT NULL,
	PASSWORD_HASH VARCHAR2 ( 50 ),
	ADDRESS VARCHAR2 ( 200 ),
CONSTRAINT ADMIN_PK PRIMARY KEY ( ID ) 
);

  
--DROP TABLE ADMIN_PHONE;

CREATE TABLE ADMIN_PHONE (
	ADMIN_ID CHAR ( 10 ),
	PHONE_NO VARCHAR2 ( 15 ),
	CONSTRAINT ADMIN_PHONE_PK PRIMARY KEY ( ADMIN_ID, PHONE_NO ),
CONSTRAINT ADMIN_PHONE_FK FOREIGN KEY ( ADMIN_ID ) REFERENCES ADMIN ( ID ) ON DELETE CASCADE 
);



INSERT INTO ADMIN(ID,LAST_NAME, FIRST_NAME, EMAIL, PASSWORD_HASH, ADDRESS) VALUEs(ID_GENERATOR.NEXTVAL,'Roy', 'KOWSHIC', 'vodro@khanabazaar.com', '123', 'dinajpur');







