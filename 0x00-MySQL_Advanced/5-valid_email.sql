-- A script that creates a trigger that resets the valid_email attribute only when the email has been changed.
DELIMITER //

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
        IF NEW.email != OLD.email THEN
	        SET New.valid_email = False;
	END IF;
END; //
