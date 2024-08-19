-- Switch to the desired database
USE hr_management;

-- Create the 'jobs' table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

-- Insert initial data into 'jobs'
INSERT INTO jobs (id, job) VALUES (1, 'Support');

-- Create the 'departments' table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

-- Create the 'hired_employees' table
CREATE TABLE IF NOT EXISTS hired_employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee VARCHAR(255),
    entry_date DATE,  -- Changed to DATE for better date handling
    department_id INT,
    job_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

