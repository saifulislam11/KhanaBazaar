CREATE TABLE "ORDER" (
         ORDER_ID CHAR(10) NOT NULL,
				 ORDER_TIME DATE NOT NULL,
				 DELIVERY_TIME DATE NOT NULL,
				 DELIVERY_LOCATION VARCHAR2(100) NOT NULL,
				 PRIMARY KEY(ORDER_ID)
				 
);