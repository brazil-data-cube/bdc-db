CREATE OR REPLACE FUNCTION update_counter()
RETURNS trigger AS $$
BEGIN
    NEW.counter = NEW.counter + 1;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_counter_fake_model
  ON fake_model;

CREATE TRIGGER update_counter_fake_model
    AFTER INSERT OR UPDATE ON fake_model
      FOR EACH ROW
    EXECUTE PROCEDURE update_counter();
