CREATE TABLE PAYS (
	ORDER_ID CHAR ( 5 ),
	PAY_ID CHAR ( 5 ),
	CONSTRAINT PAYS_PK PRIMARY KEY ( PAY_ID ),
	CONSTRAINT PAYS_ORDER_FK FOREIGN KEY ( ORDER_ID ) REFERENCES ORDER ( ID ) ON DELETE CASCADE,
CONSTRAINT PAYS_PAYMENT_FK FOREIGN KEY ( PAY_ID ) REFERENCES PAYMENT ( ID ) ON DELETE CASCADE 
);