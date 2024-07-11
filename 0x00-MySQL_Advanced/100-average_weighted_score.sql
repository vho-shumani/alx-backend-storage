-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    SELECT 
        SUM(c.score * p.weight) INTO total_weighted_score,
        SUM(p.weight) INTO total_weight
    FROM 
        corrections c
    JOIN 
        projects p ON c.project_id = p.id
    WHERE 
        c.user_id = user_id;

    UPDATE users
    SET average_score = 
        CASE 
            WHEN total_weight > 0 THEN total_weighted_score / total_weight
            ELSE 0
        END
    WHERE id = user_id;
END //

DELIMITER ;