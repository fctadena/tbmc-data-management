-- -- Insert some records into Project, Source, and Type tables first (if not already inserted)

-- -- Example insertions for Project table
-- INSERT INTO Project (project_name) VALUES
--     ('GCCD Transport Phase 1'),
--     ('FFE RARE'),
--     ('GCU+');

-- -- Example insertions for Source table
-- INSERT INTO Source (source_name) VALUES
--     ('EDP'),
--     ('RHAJTEK'),
--     ('Inhouse');

-- -- Example insertions for Type table
-- INSERT INTO Type (type_name) VALUES
--     ('PPE'),
--     ('Mobilization'),
--     ('Misc');

-- Now insert records into the Items table
INSERT INTO Items (description, man_r, unit, qty, unit_cost, amount, project_id, source_id, type_id)
VALUES
    ('Widget A1', 12.50, 'pcs', 100, 1.25, 125.00, 1, 1, 1),
    ('Gadget B1', 8.75, 'sets', 50, 5.00, 250.00, 2, 2, 2),
    ('Tool C1', 15.00, 'units', 30, 10.50, 315.00, 1, 3, 3),
    ('Material X1', 0.00, 'kg', 500, 0.75, 375.00, 3, 1, 4),
    ('Part Y1', 5.25, 'pieces', 200, 2.00, 400.00, 2, 3, 2);
