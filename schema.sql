CREATE TABLE "profile" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL,
  "date" timestamp
);

CREATE TABLE "operation" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL,
  "description" varchar
);

CREATE TABLE "tag" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL,
  "description" varchar
);

CREATE TABLE "metric" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL,
  "description" varchar
);

CREATE TABLE "profile_operation" (
  "id" SERIAL PRIMARY KEY,
  "id_report" int,
  "id_operation" int,
  "id_metric" int,
  "metric_value" float
);

CREATE TABLE "report" (
  "id" SERIAL PRIMARY KEY,
  "id_profile" int,
  "name" varchar,
  "date" timestamp,
  "description" varchar
);

CREATE TABLE "report_operation" (
  "id" SERIAL PRIMARY KEY,
  "id_report" int,
  "id_operation" int,
  "id_metric" int,
  "metric_value" float,
  "alias" varchar
);

CREATE UNIQUE INDEX "report_identifier" ON "report" ("name", "date");

CREATE TABLE "profile_tag" (
  "profile_id" int NOT NULL,
  "tag_id" int NOT NULL,
  PRIMARY KEY ("profile_id", "tag_id")
);

ALTER TABLE "profile_tag" ADD FOREIGN KEY ("profile_id") REFERENCES "profile" ("id");

ALTER TABLE "profile_tag" ADD FOREIGN KEY ("tag_id") REFERENCES "tag" ("id");


CREATE TABLE "operation_tag" (
  "operation_id" int NOT NULL,
  "tag_id" int NOT NULL,
  PRIMARY KEY ("operation_id", "tag_id")
);

ALTER TABLE "operation_tag" ADD FOREIGN KEY ("operation_id") REFERENCES "operation" ("id");

ALTER TABLE "operation_tag" ADD FOREIGN KEY ("tag_id") REFERENCES "tag" ("id");


CREATE TABLE "report_tag" (
  "report_id" int NOT NULL,
  "tag_id" int NOT NULL,
  PRIMARY KEY ("report_id", "tag_id")
);

ALTER TABLE "report_tag" ADD FOREIGN KEY ("report_id") REFERENCES "report" ("id");

ALTER TABLE "report_tag" ADD FOREIGN KEY ("tag_id") REFERENCES "tag" ("id");


ALTER TABLE "profile_operation" ADD FOREIGN KEY ("id_report") REFERENCES "operation" ("id");

ALTER TABLE "profile_operation" ADD FOREIGN KEY ("id_operation") REFERENCES "operation" ("id");

ALTER TABLE "profile_operation" ADD FOREIGN KEY ("id_metric") REFERENCES "metric" ("id");

ALTER TABLE "report" ADD FOREIGN KEY ("id_profile") REFERENCES "profile" ("id");

ALTER TABLE "report_operation" ADD FOREIGN KEY ("id_report") REFERENCES "report" ("id");

ALTER TABLE "report_operation" ADD FOREIGN KEY ("id_operation") REFERENCES "operation" ("id");

ALTER TABLE "report_operation" ADD FOREIGN KEY ("id_metric") REFERENCES "metric" ("id");
