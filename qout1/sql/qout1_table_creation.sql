-- Create the Project table
CREATE TABLE Project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) UNIQUE NOT NULL
);

-- Create the Source table
CREATE TABLE Source (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) UNIQUE NOT NULL
);

-- Create the Type table
CREATE TABLE Type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(255) UNIQUE NOT NULL
);


-- Create the Items table
CREATE TABLE Items (
    description TEXT NOT NULL,
    man_r DECIMAL(10, 2),
    unit VARCHAR(50),
    qty INTEGER,
    unit_cost DECIMAL(10, 2),
    amount DECIMAL(10, 2),
    project_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    PRIMARY KEY (description, project_id, source_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (source_id) REFERENCES Source(source_id),
	FOREIGN KEY (source_id) REFERENCES Type(type_id)

);

-- Create indexes for foreign key columns in Items table
CREATE INDEX idx_project_id ON Items(project_id);
CREATE INDEX idx_source_id ON Items(source_id);
CREATE INDEX idx_type_id ON Items(type_id);
