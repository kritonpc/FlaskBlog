BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
CREATE TABLE IF NOT EXISTS "category" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(30),
	"desctiption"	VARCHAR(256),
	"image"	VARCHAR(256),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	VARCHAR(64) NOT NULL,
	"gender"	BOOLEAN NOT NULL,
	"dob"	DATE,
	"username"	VARCHAR(64),
	"nickname"	VARCHAR(64),
	"description"	VARCHAR(256),
	"avatar"	VARCHAR(256),
	"email"	VARCHAR(120),
	"password_hash"	VARCHAR(128),
	"ip"	VARCHAR(15),
	"auth_token"	VARCHAR(32),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "post" (
	"id"	VARCHAR(64) NOT NULL,
	"title"	VARCHAR(64),
	"body"	VARCHAR(256),
	"poster_id"	VARCHAR(64),
	"category_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("category_id") REFERENCES "category"("id"),
	FOREIGN KEY("poster_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "comment" (
	"id"	VARCHAR(64) NOT NULL,
	"post_id"	VARCHAR(64),
	"user_id"	VARCHAR(64),
	"body"	VARCHAR(256),
	"timestamp"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("post_id") REFERENCES "post"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "dislike" (
	"id"	VARCHAR(64) NOT NULL,
	"post_id"	VARCHAR(64),
	"user_id"	VARCHAR(64),
	PRIMARY KEY("id"),
	FOREIGN KEY("post_id") REFERENCES "post"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "like" (
	"id"	VARCHAR(64) NOT NULL,
	"post_id"	VARCHAR(64),
	"user_id"	VARCHAR(64),
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("post_id") REFERENCES "post"("id")
);
INSERT INTO "alembic_version" VALUES ('679ec739d262');
INSERT INTO "alembic_version" VALUES ('85876f52a7bf');
INSERT INTO "category" VALUES (1,'Gaming','Everything about gaming','categories/gaming.jpg');
INSERT INTO "category" VALUES (2,'Animals','Everything about animals','categories/animals.jpg');
INSERT INTO "category" VALUES (3,'News','News around the world','categories/news.jpg');
INSERT INTO "category" VALUES (4,'Food','Delicious food','categories/food.jpg');
INSERT INTO "user" VALUES ('07196a56-08b9-4952-9986-694f9b90a10e',1,NULL,'admin','The Admin','Just your admin','admin.jpg','admin@flex.gr','fed0817a288ea3421520ac1b22ae1e7cd938cfe13ef9a01ba51011a61ad8b42b','127.0.0.1','0136f5124a0e44b8b05025f66a0af6ec');
INSERT INTO "user" VALUES ('5277cb77-615c-4462-a8d3-7d37b6c5e7fe',1,NULL,'kritonpc','Karkinos','Exw gene8lia 5/7','avatar.png','paranoidhax@gmail.com','a5dcd224e35fd4a994a4db49d90563f386658b441b27f7d9ed1b6fd906071bab','127.0.0.1',NULL);
INSERT INTO "user" VALUES ('19d117f6-b704-4eac-acf3-47ab207a1584',1,'2017-07-05','karkiniarhs','Karkinwpos','Den exw idea ti kanw edw mesa','avatar.png','karkos@flexpie.ao','a5dcd224e35fd4a994a4db49d90563f386658b441b27f7d9ed1b6fd906071bab','127.0.0.1',NULL);
INSERT INTO "post" VALUES ('1','The first post','This is the first post of this website','07196a56-08b9-4952-9986-694f9b90a10e',1);
INSERT INTO "post" VALUES ('a1008395-61d1-4256-8e72-d3ada37c75db','The first web post','This is the first post created from the web app','07196a56-08b9-4952-9986-694f9b90a10e',1);
INSERT INTO "post" VALUES ('06193f3f-35a6-44b4-aff9-0fa0219e5485','The second web post','Pretty much what the title says','07196a56-08b9-4952-9986-694f9b90a10e',1);
INSERT INTO "post" VALUES ('92d9d8d6-4e32-495a-8f74-96831f9e3fc7','The third web post','This is the... ahh no need for that','07196a56-08b9-4952-9986-694f9b90a10e',1);
INSERT INTO "post" VALUES ('704e118d-61dc-4a22-bb6a-d3f6fa68c4ad','Darras Vibes','At location Darras Market','07196a56-08b9-4952-9986-694f9b90a10e',1);
INSERT INTO "post" VALUES ('b22a182e-75a5-45f3-aea1-cd5594c884aa','I don''t even know why I''m posting here','This ain''t even an animal related post','07196a56-08b9-4952-9986-694f9b90a10e',2);
INSERT INTO "post" VALUES ('1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','8elw na faw saraglakia','alla exw dyslexia','07196a56-08b9-4952-9986-694f9b90a10e',4);
INSERT INTO "comment" VALUES ('1','704e118d-61dc-4a22-bb6a-d3f6fa68c4ad','07196a56-08b9-4952-9986-694f9b90a10e','Karkovic',NULL);
INSERT INTO "comment" VALUES ('881e4388-770c-450e-b7e3-298a6937ac77','a1008395-61d1-4256-8e72-d3ada37c75db','07196a56-08b9-4952-9986-694f9b90a10e','Test','2021-12-29 15:39:21.729676');
INSERT INTO "comment" VALUES ('0f79f590-2bfe-49fa-a8e8-51d36642454a','06193f3f-35a6-44b4-aff9-0fa0219e5485','07196a56-08b9-4952-9986-694f9b90a10e','Lol cringe','2021-12-29 15:46:49.561795');
INSERT INTO "comment" VALUES ('cbd3dff9-bb11-4200-8032-d6b01a0403b4','b22a182e-75a5-45f3-aea1-cd5594c884aa','07196a56-08b9-4952-9986-694f9b90a10e','Karkinos','2021-12-29 15:51:47.122373');
INSERT INTO "comment" VALUES ('d7ec80c2-da86-4ed6-9ea7-19b2d10d718e','b22a182e-75a5-45f3-aea1-cd5594c884aa','07196a56-08b9-4952-9986-694f9b90a10e','Karkinos
','2021-12-29 15:52:01.774710');
INSERT INTO "comment" VALUES ('713e4b9f-48fa-48b5-85ff-6b556ff40c05','b22a182e-75a5-45f3-aea1-cd5594c884aa','07196a56-08b9-4952-9986-694f9b90a10e','5/7
','2021-12-29 15:52:09.365768');
INSERT INTO "comment" VALUES ('09746aa6-d28c-4054-ae2e-a66d306cd513','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e','Karkinos
','2021-12-29 15:59:01.635189');
INSERT INTO "comment" VALUES ('da153b97-15e4-4545-82a0-7c4c95d27e1e','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e','
','2021-12-29 15:59:03.615249');
INSERT INTO "comment" VALUES ('3f8b72c8-2959-4384-a6dd-54bea4363e4c','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e','asdasdasd','2021-12-29 15:59:27.475955');
INSERT INTO "comment" VALUES ('e5991752-93f1-4887-bec4-adf6ce274a3e','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e','asd','2021-12-29 16:00:25.083846');
INSERT INTO "comment" VALUES ('60abf7c9-c9fc-40c8-a57c-cf54d41ccd47','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e','teso
','2021-12-29 16:01:22.422846');
INSERT INTO "dislike" VALUES ('fd648234-51d4-4691-b312-abffa4c4cf6c','704e118d-61dc-4a22-bb6a-d3f6fa68c4ad','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('b92e6736-92c4-46cb-8879-894adee06e05','92d9d8d6-4e32-495a-8f74-96831f9e3fc7','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('25cfd26c-7d6a-447d-b45d-afc3894cf9f0','1','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('f93dfc22-1e63-4f75-b4fb-69f0f908d7a0','b22a182e-75a5-45f3-aea1-cd5594c884aa','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('739f42de-073a-4c36-b82a-0fe0c2d18470','06193f3f-35a6-44b4-aff9-0fa0219e5485','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('2e8aaecd-2001-4049-8298-1eb658d1a048','a1008395-61d1-4256-8e72-d3ada37c75db','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "dislike" VALUES ('83a38a3c-e911-494c-9076-80b74a2dac5a','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('5793dd0a-6364-4fc6-b479-8ba33784e33d','704e118d-61dc-4a22-bb6a-d3f6fa68c4ad','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('1dabe612-d809-4feb-9082-754c95e7297e','92d9d8d6-4e32-495a-8f74-96831f9e3fc7','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('4a72824e-93f3-4c81-89fd-1072a6e0ed17','a1008395-61d1-4256-8e72-d3ada37c75db','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('3a520b07-7b0e-4e17-8e3d-54ce781d87dc','1','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('2221b5e4-968f-42b2-bb44-1ec00b9df465','06193f3f-35a6-44b4-aff9-0fa0219e5485','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('5b394245-1eb0-461c-a6bc-1e639520ba59','b22a182e-75a5-45f3-aea1-cd5594c884aa','07196a56-08b9-4952-9986-694f9b90a10e');
INSERT INTO "like" VALUES ('f9064fa1-bf53-4161-bac5-64a9e30b3e62','1fcd5065-4be9-470e-ab7f-5cb25e94ee2b','07196a56-08b9-4952-9986-694f9b90a10e');
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_auth_token" ON "user" (
	"auth_token"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_email" ON "user" (
	"email"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_nickname" ON "user" (
	"nickname"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_username" ON "user" (
	"username"
);
CREATE INDEX IF NOT EXISTS "ix_comment_timestamp" ON "comment" (
	"timestamp"
);
COMMIT;
