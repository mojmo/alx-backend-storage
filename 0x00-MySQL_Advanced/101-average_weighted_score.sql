-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUsers

-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_avg FLOAT;
    
    -- Cursor to iterate over each user
    DECLARE cur CURSOR FOR 
        SELECT id FROM users;
    
    -- Declare continue handler to exit loop
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Open the cursor
    OPEN cur;
    
    -- Start fetching rows
    fetch_loop: LOOP
        -- Initialize variables for each iteration
        SET done = 0;
        SET total_score = 0;
        SET total_weight = 0;
        SET weighted_avg = 0;
        
        -- Fetch user_id from cursor
        FETCH cur INTO user_id;
        
        -- Check if we are done fetching
        IF done = 1 THEN
            LEAVE fetch_loop;
        END IF;
        
        -- Calculate the total weighted score and total weight for the user
        SELECT 
            SUM(c.score * p.weight),
            SUM(p.weight)
        INTO 
            total_score,
            total_weight
        FROM 
            corrections c
            JOIN projects p ON c.project_id = p.id
        WHERE 
            c.user_id = user_id;
        
        -- Calculate the weighted average score if total_weight is not zero
        IF total_weight > 0 THEN
            SET weighted_avg = total_score / total_weight;
        END IF;
        
        -- Update the average_score for the user in the users table
        UPDATE users
        SET average_score = weighted_avg
        WHERE id = user_id;
    END LOOP;
    
    -- Close cursor
    CLOSE cur;
    
END //

DELIMITER ;
