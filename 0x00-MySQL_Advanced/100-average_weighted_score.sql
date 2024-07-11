-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_score_sum FLOAT DEFAULT 0;

    SELECT 
        SUM(p.weight) INTO total_weight,
        SUM(c.score * p.weight) INTO weighted_score_sum
    FROM 
        corrections c
    JOIN 
        projects p ON c.project_id = p.id
    WHERE 
        c.user_id = user_id;

    DECLARE average_weighted_score FLOAT DEFAULT 0;
    IF total_weight > 0 THEN
        SET average_weighted_score = weighted_score_sum / total_weight;
    END IF;

    UPDATE 
        users
    SET 
        average_score = average_weighted_score
    WHERE 
        id = user_id;
END //

DELIMITER ;
