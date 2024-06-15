-- This  SQL script creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN input_user_id INT)
BEGIN
	DECLARE avg_score DECIMAL(10, 2);
	SELECT ROUND(AVG(score), 2) INTO avg_score
	FROM corrections
	WHERE user_id = input_user_id;

	UPDATE users
	SET average_score = avg_score
	WHERE id = input_user_id;
END$$

DELIMITER ;
