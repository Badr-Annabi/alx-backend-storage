-- This SQL script creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE total_weight_score FLOAT;
	DECLARE total_weight INT;

	SELECT SUM(c.score * p.weight) INTO total_weight_score
	FROM corrections c
	JOIN projects p ON c.project_id = p.id
	WHERE c.user_id = user_id;

	SELECT SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

	UPDATE users
	SET average_score = IF(total_weight = 0, 0, total_weight_score / total_weight)
	WHERE id = user_id;
END$$

DELIMITER ;
