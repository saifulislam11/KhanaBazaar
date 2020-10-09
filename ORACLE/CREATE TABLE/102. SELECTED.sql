CREATE TABLE SELECTED (
	ORDER_ID CHAR ( 5 ),
	FOOD_ID CHAR ( 5 ),
	CONSTRAINT SELECTED_PK PRIMARY KEY ( ORDER_ID, FOOD_ID ),
	CONSTRAINT SELECTED_ORDER_FK FOREIGN KEY ( ORDER_ID ) REFERENCES ORDER ( ID ) ON DELETE CASCADE,
	CONSTRAINT SELECTED_FOOD_FK FOREIGN KEY ( FOOD_ID ) REFERENCES FOOD_ITEM ( ID ) --  ON DELETE ??

);