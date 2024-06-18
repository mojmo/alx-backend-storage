-- This script create a stored procedure ComputeAverageWeightedScoreForUser

-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_avg FLOAT DEFAULT 0;
    
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
    
END //

DELIMITER ;
