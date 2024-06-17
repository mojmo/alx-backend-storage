-- Create stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_count INT;
    DECLARE avg_score DECIMAL(10, 2);

    -- Compute total score and count of corrections for the user
    SELECT SUM(score), COUNT(*)
    INTO total_score, total_count
    FROM corrections
    WHERE user_id = p_user_id;

    -- Calculate average score
    IF total_count > 0 THEN
        SET avg_score = total_score / total_count;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the average_score in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = p_user_id;
END //

DELIMITER ;
