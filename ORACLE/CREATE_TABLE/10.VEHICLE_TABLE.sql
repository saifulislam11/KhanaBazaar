CREATE TABLE VEHICLE(
          ID CHAR(10) NOT NULL,
					REG_NO CHAR(15) NOT NULL,
					"TYPE" VARCHAR2(50),
					CONSTRAINT VEHICLE_PK PRIMARY KEY(ID)
);
INSERT INTO VEHICLE(ID,REG_NO,TYPE) VALUES('1000000000','123123123123123','RICKSHAW');