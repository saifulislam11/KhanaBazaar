CREATE TABLE CONTRACT(
             ID CHAR(10) NOT NULL,
						 DURATION INTEGER,
						 SALARY FLOAT NOT NULL,
						 INIT_RATING INTEGER CHECK (INIT_RATING BETWEEN 0 AND 5),
						 DATE_OF_CONTRACT DATE,
						 CONSTRAINT CONTRACT_PK PRIMARY KEY(ID)
);