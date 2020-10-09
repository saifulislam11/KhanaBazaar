CREATE TABLE REVIEW(
         ID CHAR(10) NOT NULL,
				 FOOD_RATING INTEGER CHECK (FOOD_RATING BETWEEN 0 AND 5) NOT NULL,
				 "COMMENT" VARCHAR2(100) ,
				 DATE_TIME DATE ,
				 CONSTRAINT REVIEW_PK PRIMARY KEY(ID)
);

--IMAGE
CREATE TABLE REVIEW_IMAGE(
        REVIEW_ID CHAR(10) NOT NULL,
				IMAGE_PATH VARCHAR2(200) NOT NULL,
				CONSTRAINT IMAGE_PK PRIMARY KEY(REVIEW_ID,IMAGE_PATH),
				FOREIGN KEY(REVIEW_ID) REFERENCES REVIEW(ID) ON DELETE CASCADE
);