CREATE TABLE USES (
	ORDER_ID CHAR ( 5 ),
	PROMO_ID CHAR ( 5 ),
	CONSTRAINT USES_PK PRIMARY KEY ( ORDER_ID ),
	CONSTRAINT USES_ORDER_FK FOREIGN KEY ( ORDER_ID ) REFERENCES ORDER ( ID ) ON DELETE CASCADE,
	CONSTRAINT USES_PROMO_FK FOREIGN KEY ( PROMO_ID ) REFERENCES PROMO ( ID ) ON DELETE 
SET NULL 
	);