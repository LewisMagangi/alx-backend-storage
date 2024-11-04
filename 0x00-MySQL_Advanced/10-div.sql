-- A script that creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.
DELIMITER //

CREATE FUNCTION SafeDiv()
RETURNS INTEGER
NOT DETERMINISTIC
BEGIN
   DECLARE DIV INTEGER
   SET DIV = a / b
   RETURN DIV
END //

DELIMITER ;
