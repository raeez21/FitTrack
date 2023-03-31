CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1000;


CREATE TABLE IF NOT EXISTS "Users" (
	"userID" BIGINT DEFAULT nextval('user_id_seq') PRIMARY KEY,
	"email" VARCHAR (255) UNIQUE NOT NULL,
	"pwd" VARCHAR (50) NOT NULL,
	"firstName" VARCHAR (50) NOT NULL,
	"lastName" VARCHAR (50) NOT NULL,
	"gender" char(10),
	"dob" Date,
	"targetCalorieIntake" Float,
	"targetCalorieBurn" Float,
	"targetCarbohydrateIntake" Float,
	"targetProteinIntake" Float,
	"targetFatIntake" Float,
	"created_on" TIMESTAMP NOT NULL DEFAULT now()
);
--ALTER TABLE "Users" ALTER COLUMN created_on SET DEFAULT now();

CREATE TABLE IF NOT EXISTS "Food" (
	"foodID" SERIAL PRIMARY KEY,
	"name" varchar (50) UNIQUE NOT NULL,
	"carbohydratesPerServing" Float NOT NULL,
	"caloriesPerServing" FLOAT NOT NULL,
	"proteinsPerServing" FLOAT NOT NULL,
	"fatPerServing" FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Exercises" (
	"exerciseID" SERIAL PRIMARY KEY,
	"name" varchar(50) UNIQUE NOT NULL,
	"caloriesBurnedPerMin" FLOAT NOT NULL,
	"url" varchar(100)
);

CREATE TABLE "FoodLog"
(
	"userID" BIGINT NOT NULL REFERENCES "Users"("userID"),
	"name" varchar (50) NOT NULL REFERENCES "Food"("name"),
	"Date" Date NOT NULL,
	Quantity INT
);

CREATE TABLE "ExerciseLog"
(
 	"userID" BIGINT NOT NULL REFERENCES "Users"("userID"),
	"name" varchar (50) NOT NULL REFERENCES "Exercises"("name"),
	Date Date NOT NULL,
	Minutes FLOAT
);

CREATE TABLE IF NOT EXISTS "BodyMeasurements" (
	"measurementID" BIGSERIAL PRIMARY KEY,
	"userID" BIGINT NOT NULL REFERENCES "Users"("userID"),
	"date" Date NOT NULL,
	"height" FLOAT,
	"weight" FLOAT,
	"waist" FLOAT,
	"hip" FLOAT,
	"bmi" FLOAT,
	"waistToHipRatio" FLOAT,
	"waistToHeightRatio" FLOAT
);

/*drop table "Users" CASCADE;
drop table "Exercises" CASCADE;
drop table "Food" CASCADE;
drop table "BodyMeasurements";
drop table "FoodLog";
drop table "ExerciseLog"; */
