CREATE TABLE FOODMAN(
       FOODMAN_ID CHAR(10) NOT NULL,
			 NAME VARCHAR2(40) NOT NULL,
			 EMAIL VARCHAR2(50) UNIQUE NOT NULL,
			 PASSWORD_HASH VARCHAR2(100) NOT NULL,
			 RATING INTEGER CHECK (RATING BETWEEN 0 AND 5),
			 IMAGE_PATH VARCHAR2(200),
			 CONSTRAINT FOODMAN_PK PRIMARY KEY(FOODMAN_ID) 
);

--FOODMAN PHONE
CREATE TABLE FOODMAN_PHONE(
          FOODMAN_ID CHAR(10) NOT NULL,
					PHONE_NO VARCHAR2(15) NOT NULL,
					CONSTRAINT PHONE_PK PRIMARY KEY(FOODMAN_ID,PHONE_NO),
					FOREIGN KEY(FOODMAN_ID) REFERENCES FOODMAN(FOODMAN_ID)
);