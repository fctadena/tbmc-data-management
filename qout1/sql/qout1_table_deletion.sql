-- Drop the indexes first
DROP INDEX IF EXISTS idx_project_id;
DROP INDEX IF EXISTS idx_source_id;
DROP INDEX IF EXISTS idx_type_id;

-- Drop the Items table
DROP TABLE IF EXISTS Items;

-- Drop the foreign key constraints (if they were named explicitly)
-- ALTER TABLE Items DROP CONSTRAINT constraint_name;

-- Drop the Project table
DROP TABLE IF EXISTS Project;

-- Drop the Source table
DROP TABLE IF EXISTS Source;

-- Drop the Type table
DROP TABLE IF EXISTS Type;
