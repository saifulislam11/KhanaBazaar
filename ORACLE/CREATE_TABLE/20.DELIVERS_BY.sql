CREATE TABLE DELIVERS_BY(
				 FOODMAN_ID CHAR(10) NOT NULL,
				 VEHICLE_ID CHAR(10),
				 CONSTRAINT DELIVERS_BY_PK PRIMARY KEY(FOODMAN_ID),
				 FOREIGN KEY(FOODMAN_ID) REFERENCES FOODMAN(ID) ON DELETE CASCADE,
				 FOREIGN KEY(VEHICLE_ID) REFERENCES VEHICLE(ID) ON DELETE CASCADE
);