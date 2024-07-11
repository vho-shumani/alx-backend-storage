-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER $$
-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS CalculateAverageWeightedScore;
CREATE PROCEDURE CalculateAverageWeightedScore(IN user_id INT)
BEGIN
    -- Update the average_score field in the users table
    UPDATE users 
    SET average_score = (
        SELECT
            SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections
        INNER JOIN projects ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id
    )
    WHERE users.id = user_id;
END $$
DELIMITER ;

