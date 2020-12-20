-- name: get-task-by-id^
SELECT id,
       description,
       category,
       is_complete,
       created_at,
       updated_at
FROM tasks
WHERE id = :id
LIMIT 1;

-- name: get-all-tasks
SELECT id,
       description,
       category,
       is_complete,
       created_at,
       updated_at
FROM tasks;

-- name: create-new-task<!
INSERT INTO tasks (description, category, is_complete)
VALUES (:description, :category, :is_complete)
RETURNING
    id, created_at, updated_at;

-- name: update-task-by-id<!
UPDATE
    tasks
SET description        = :description,
    category           = :category,
	is_complete        = :is_complete,\
WHERE id = :id
RETURNING
    updated_at;

-- name: delete-task-by-id!
DELETE FROM tasks WHERE id = :id