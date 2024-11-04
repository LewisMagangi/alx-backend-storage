--  a SQL script that creates an index idx_name_first on the table names and the first letter of name
CREATE INDEX index_name_first_score on names (name(1));
