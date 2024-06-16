-- This SQL script creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for sll student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser()
BEGIN
	DECLARE done INT DEFAULT 0;
	DECLARE user_id INT;
	DECLARE total_weight_score FLOAT;
	DECLARE total_weight INT;
	DECLARE cur CURSOR FOR SELECT id FROM users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

	OPEN cur;

	read_loop: LOOP
		FETCH cur INTO user_id;
		IF done THEN
			LEAVE read_loop;
		END IF

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
	END LOOP;

	CLOSE cur;
END$$

DELIMITER ;
