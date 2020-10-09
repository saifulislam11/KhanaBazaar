CREATE TABLE PROMO(
        ID CHAR(10) NOT NULL,
				NAME VARCHAR2(30) NOT NULL,
				"PERCENT" INTEGER,
				FIXED_AMOUNT FLOAT NOT NULL,
				PROMO_LIMIT INTEGER NOT NULL,
				MIN_ORDER_VALUE FLOAT NOT NULL,
				MAX_DISCOUNT_AMOUNT FLOAT NOT NULL,
				CONSTRAINT PROMO_PK PRIMARY KEY(ID)
);