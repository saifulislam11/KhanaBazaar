CREATE TABLE RESTAURANT(
    RESTAURANT_ID CHAR(10) NOT NULL,
		NAME VARCHAR2(40) NOT NULL,
		LOCATION VARCHAR2(100) NOT NULL,
		LOGO_PATH VARCHAR2(100) NOT NULL,
		RATING INTEGER CHECK (RATING BETWEEN 0 AND 5),
		OPEN_TIME VARCHAR2(40) NOT NULL,
		CLOSE_TIME VARCHAR2(40) NOT NULL,
		EMAIL VARCHAR2(50) UNIQUE NOT NULL,
		PASSWORD_HASH VARCHAR2(40) NOT NULL,
		PRIMARY KEY (RESTAURANT_ID)
);