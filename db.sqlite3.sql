BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2025-02-27 17:13:14.203784');
INSERT INTO "django_migrations" VALUES (2,'contenttypes','0002_remove_content_type_name','2025-02-27 17:13:14.210791');
INSERT INTO "django_migrations" VALUES (3,'auth','0001_initial','2025-02-27 17:13:14.225803');
INSERT INTO "django_migrations" VALUES (4,'auth','0002_alter_permission_name_max_length','2025-02-27 17:13:14.234812');
INSERT INTO "django_migrations" VALUES (5,'auth','0003_alter_user_email_max_length','2025-02-27 17:13:14.242818');
INSERT INTO "django_migrations" VALUES (6,'auth','0004_alter_user_username_opts','2025-02-27 17:13:14.248824');
INSERT INTO "django_migrations" VALUES (7,'auth','0005_alter_user_last_login_null','2025-02-27 17:13:14.258337');
INSERT INTO "django_migrations" VALUES (8,'auth','0006_require_contenttypes_0002','2025-02-27 17:13:14.262341');
INSERT INTO "django_migrations" VALUES (9,'auth','0007_alter_validators_add_error_messages','2025-02-27 17:13:14.268346');
INSERT INTO "django_migrations" VALUES (10,'auth','0008_alter_user_username_max_length','2025-02-27 17:13:14.278355');
INSERT INTO "django_migrations" VALUES (11,'auth','0009_alter_user_last_name_max_length','2025-02-27 17:13:14.288364');
INSERT INTO "django_migrations" VALUES (12,'auth','0010_alter_group_name_max_length','2025-02-27 17:13:14.297372');
INSERT INTO "django_migrations" VALUES (13,'auth','0011_update_proxy_permissions','2025-02-27 17:13:14.312385');
INSERT INTO "django_migrations" VALUES (14,'auth','0012_alter_user_first_name_max_length','2025-02-27 17:13:14.320392');
INSERT INTO "django_migrations" VALUES (15,'sessions','0001_initial','2025-02-27 17:13:14.326901');
INSERT INTO "django_content_type" VALUES (1,'auth','permission');
INSERT INTO "django_content_type" VALUES (2,'auth','group');
INSERT INTO "django_content_type" VALUES (3,'auth','user');
INSERT INTO "django_content_type" VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (5,'sessions','session');
INSERT INTO "auth_permission" VALUES (1,1,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (2,1,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (3,1,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (4,1,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (5,2,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (6,2,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (7,2,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (8,2,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (9,3,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (10,3,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (11,3,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (12,3,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (20,5,'view_session','Can view session');
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;
