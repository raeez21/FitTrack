CREATE TRIGGER targets_history_trigger
AFTER INSERT OR UPDATE ON "Profile"
FOR EACH ROW
EXECUTE FUNCTION targets_history_insert();