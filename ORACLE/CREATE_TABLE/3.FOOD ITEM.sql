
CREATE TABLE FOOD_ITEM (
	ID CHAR ( 10 ) UNIQUE,
	RESTAURANT_ID CHAR(10) NOT NULL,
	NAME VARCHAR2 ( 50 ) NOT NULL,
	PRICE INTEGER CHECK(PRICE > 0) NOT NULL,
	OFFER INTEGER,
	AVAILIBILITY CHAR ( 1 ),
	DESCRIPTION VARCHAR2 ( 1000 ),
	"TYPE" VARCHAR2 ( 50 ),
	CONSTRAINT FOOD_ITEM_PK PRIMARY KEY(ID,RESTAURANT_ID),
	FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANT(ID) ON DELETE CASCADE
		
);

CREATE TABLE FOOD_ITEM_PATH (
	ID CHAR ( 10 ),
	IMAGE_PATH VARCHAR2 ( 200 ),
	CONSTRAINT FOOD_ITEM_PATH_PK PRIMARY KEY ( ID, IMAGE_PATH ),
CONSTRAINT FOOD_ITEM_PATH_FK FOREIGN KEY ( ID ) REFERENCES FOOD_ITEM ( ID ) ON DELETE CASCADE 
);