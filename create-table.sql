Create table customer_info(
	email varchar(50)NOT NULL,
	fname varchar(30),
	lname varchar(15),
	pass varchar(15),
	phone varchar(15),
	area varchar(30),
	town varchar(30),
	status varchar(10),
	PRIMARY KEY(email)
);

Create table order_info(
	order_id varchar(5)NOT NULL,
	email varchar(50),
	TORCV Date,
	TODEL Date,
	PRIMARY KEY (order_id),
	FOREIGN KEY (email) References customer_info (email)
);

Create table management(
 	user_id varchar(30)NOT NULL,
 	pass varchar(15),
 	user_name varchar(50),
 	status varchar(10),
 	designation varchar(15),
 	PRIMARY KEY (user_id)
 );

Create table menu(
	item_id varchar(7)NOT NULL,
	item_name varchar(30),
	description varchar(30),
	price money,
	category varchar(20),
	status varchar(10),
	user_id varchar(30),
	PRIMARY KEY (item_id),
	FOREIGN KEY (user_id) References management(user_id)
);

Create table order_items(
 	order_id varchar(5) NOT NULL,
 	item_id varchar(7) NOT NULL,
 	quantity int4,
 	status varchar(15),
 	user_id varchar(30),
 	PRIMARY KEY ( order_id, item_id )
 );