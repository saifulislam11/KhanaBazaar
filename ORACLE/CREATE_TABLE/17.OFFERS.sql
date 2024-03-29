  
CREATE TABLE OFFERS(
          ADMIN_ID CHAR(10) NOT NULL,
					CUSTOMER_ID CHAR(10),
					PROMO_ID CHAR(10),
					CONSTRAINT OFFERS_PK PRIMARY KEY(CUSTOMER_ID,PROMO_ID),
					FOREIGN KEY(ADMIN_ID) REFERENCES ADMIN(ID) ON DELETE CASCADE,
					FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(ID) ON DELETE CASCADE,
					FOREIGN KEY(PROMO_ID) REFERENCES PROMO(ID) ON DELETE CASCADE	
);