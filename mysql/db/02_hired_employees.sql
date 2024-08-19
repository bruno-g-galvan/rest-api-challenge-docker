CREATE TABLE hired_employees (
    id INT NOT NULL AUTO_INCREMENT,
    employee VARCHAR(255),
    entry_date VARCHAR(255),
    department_id INT,
    job_id INT,
    PRIMARY KEY (id)
);