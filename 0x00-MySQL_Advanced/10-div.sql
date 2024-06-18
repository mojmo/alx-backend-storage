-- Create a function SafeDiv that divides two integers safely, returning 0 if the divisor is zero.

DROP FUNCTION IF EXISTS SafeDiv;

DELIMITER //

-- Create the function SafeDiv
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    -- Check if the divisor (b) is zero
    IF b = 0 THEN
        -- If divisor is zero, set result to 0
        RETURN (0);
    ELSE
        -- If divisor is not zero, compute the division
        RETURN (a / b);
    END IF;

END //

DELIMITER ;
