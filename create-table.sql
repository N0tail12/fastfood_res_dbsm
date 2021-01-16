CREATE TABLE "customer_info" (
  "email" varchar(20) PRIMARY KEY NOT NULL,
  "fname" varchar(12),
  "lname" varchar(12),
  "pass" varchar(15),
  "phone" varchar(14),
  "area" varchar(10),
  "town" varchar(10),
  "status" varchar(10)
);

CREATE TABLE "order_info" (
  "order_id" varchar(5) PRIMARY KEY NOT NULL,
  "email" varchar(20),
  "TORCV" Date,
  "TODEL" Date
);

CREATE TABLE "management" (
  "user_id" varchar(20) PRIMARY KEY NOT NULL,
  "pass" varchar(15),
  "user_name" varchar(15),
  "status" varchar(5),
  "designation" varchar(8)
);

CREATE TABLE "menu" (
  "item_id" varchar(7) PRIMARY KEY NOT NULL,
  "item_name" varchar(15),
  "description" varchar(30),
  "price" money,
  "catagory" varchar(8),
  "status" varchar(10),
  "user_id" varchar(20)
);

CREATE TABLE "order_items" (
  "order_id" varchar(5) NOT NULL,
  "item_id" varchar(7) NOT NULL,
  "quantity" int4,
  "status" varchar(10),
  "user_id" varchar(20),
  PRIMARY KEY ("order_id", "item_id")
);

ALTER TABLE "order_info" ADD FOREIGN KEY ("email") REFERENCES "customer_info" ("email");

ALTER TABLE "menu" ADD FOREIGN KEY ("user_id") REFERENCES "management" ("user_id");

ALTER TABLE "order_items" ADD FOREIGN KEY ("order_id") REFERENCES "order_info" ("order_id");

ALTER TABLE "order_items" ADD FOREIGN KEY ("user_id") REFERENCES "management" ("user_id");

ALTER TABLE "order_items" ADD FOREIGN KEY ("item_id") REFERENCES "menu" ("item_id");

