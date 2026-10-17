-- Add a subject
INSERT INTO subjects (name, color)
VALUES ('Database Systems', '#e10600');

-- Add a study session
INSERT INTO study_sessions (subject_id, minutes, session_date)
VALUES (1, 30, '2026-10-16');

-- Display all subjects
SELECT *
FROM subjects;

-- Display sessions with their subject names
SELECT
    study_sessions.id,
    subjects.name AS subject_name,
    study_sessions.minutes,
    study_sessions.session_date
FROM study_sessions
JOIN subjects
    ON study_sessions.subject_id = subjects.id;

-- Calculate total study time
SELECT COALESCE(SUM(minutes), 0) AS total_minutes
FROM study_sessions;

-- Find the total time for each subject
SELECT
    subjects.name,
    SUM(study_sessions.minutes) AS total_minutes
FROM subjects
JOIN study_sessions
    ON subjects.id = study_sessions.subject_id
GROUP BY subjects.id, subjects.name;

-- Update a study session
UPDATE study_sessions
SET minutes = 45
WHERE id = 1;

-- Delete a study session
DELETE FROM study_sessions
WHERE id = 1;

-- Find subjects with at least one study session
SELECT name
FROM subjects
WHERE id IN (
    SELECT subject_id
    FROM study_sessions
);
