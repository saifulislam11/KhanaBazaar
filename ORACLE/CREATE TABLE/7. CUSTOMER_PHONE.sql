CREATE TABLE CUSTOMER_PHONE (
	CUSTOMER_ID VARCHAR2 ( 15 ),
	PHONE_NO VARCHAR2 ( 15 ),
	CONSTRAINT CUSTOMER_PHONE_PK PRIMARY KEY ( CUSTOMER_ID, PHONE_NO ),
CONSTRAINT CUSTOMER_PHONE_FK FOREIGN KEY ( CUSTOMER_ID ) REFERENCES CUSTOMER ( ID ) 
);