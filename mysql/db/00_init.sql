-- Switch to the desired database
USE hr_management;

-- Create the 'jobs' table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

-- Create the 'departments' table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

-- Create the 'hired_employees' table
CREATE TABLE IF NOT EXISTS hired_employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee VARCHAR(255),
    entry_date VARCHAR(255),
    department_id INT,
    job_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);


LOAD DATA INFILE '/var/lib/mysql-files/departments.csv'
INTO TABLE departments 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE '/var/lib/mysql-files/jobs.csv' 
INTO TABLE jobs 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE '/var/lib/mysql-files/hired_employees.csv'
INTO TABLE hired_employees 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
(id, employee, entry_date, @department_id, @job_id)
SET 
department_id = NULLIF(@department_id, ''),
job_id = NULLIF(@job_id, '');
