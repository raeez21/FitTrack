CREATE OR REPLACE FUNCTION targets_history_insert()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'UPDATE' THEN
    IF NEW."target_calorie_intake" IS DISTINCT FROM OLD."target_calorie_intake" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_calorie_intake', NEW."target_calorie_intake", NOW());
    END IF;
	IF NEW."target_calorie_burn" IS DISTINCT FROM OLD."target_calorie_burn" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_calorie_burn', NEW."target_calorie_burn", NOW());
    END IF;
    
    IF NEW."target_protein_intake" IS DISTINCT FROM OLD."target_protein_intake" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_protein_intake', NEW."target_protein_intake", NOW());
    END IF;
	IF NEW."target_fat_intake" IS DISTINCT FROM OLD."target_fat_intake" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_fat_intake', NEW."target_fat_intake", NOW());
    END IF;
	IF NEW."target_carbohydrate_intake" IS DISTINCT FROM OLD."target_carbohydrate_intake" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_carbohydrate_intake', NEW."target_carbohydrate_intake", NOW());
    END IF;
	IF NEW."target_water_intake" IS DISTINCT FROM OLD."target_water_intake" THEN
      INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
      VALUES (OLD.user_id, 'target_water_intake', NEW."target_water_intake", NOW());
    END IF;
    
    -- add more IF statements for other Target fields if needed
  ELSIF TG_OP = 'INSERT' THEN
    INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_calorie_intake', NEW."target_calorie_intake", NOW());
    INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_calorie_burn', NEW."target_calorie_burn", NOW());
	INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_protein_intake', NEW."target_protein_intake", NOW());
	INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_fat_intake', NEW."target_fat_intake", NOW());
	INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_carbohydrate_intake', NEW."target_carbohydrate_intake", NOW());
	INSERT INTO "TargetsHistory" (user_profile_id, target_type, target_value, created_on)
    VALUES (NEW.id, 'target_water_intake', NEW."target_water_intake", NOW());
    -- add more INSERT statements for other Target fields if needed
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;