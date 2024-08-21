
# Overview

This Flask-based REST API application provides endpoints to interact with a MySQL database. It is designed to retrieve and publish data in JSON format, including job information, department details, hired employees, and specific queries related to hired employees in 2021.

## Components

### Flask Framework

- The application uses Flask to handle HTTP requests and serve responses. Flask is a lightweight WSGI web application framework in Python.

### MySQL Connector

- `mysql.connector` is used to connect to the MySQL database and execute SQL queries. The connection configuration is provided via environment variables.

### Environment Variables

- Database connection parameters such as `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` are retrieved from environment variables.

### Endpoints

- **`/jobs`**: Retrieves all job entries from the `jobs` table and returns them as a list of JSON objects with `id` and `job` fields.
- **`/departments`**: Retrieves all department entries from the `departments` table and returns them as a list of JSON objects with `id` and `department` fields.
- **`/hired_employees`**: Retrieves all entries from the `hired_employees` table and returns them as a list of JSON objects with `id`, `employee`, `entry_date`, `department_id`, and `job_id` fields.
- **`/hired_employees_2021_quarters`**: Retrieves hiring statistics for 2021, aggregated by department and job, and counts hires per quarter. Returns data as a list of JSON objects with `department`, `job`, `Q1`, `Q2`, `Q3`, and `Q4` fields.
- **`/hired_employees_2021`**: Retrieves departments with hiring counts greater than the average number of hires for 2021 and returns data as a list of JSON objects with `id`, `department`, and `hired` fields.

### Error Handling

- **Database Errors**: Catches and prints MySQL connection errors and returns an appropriate message.
- **Unexpected Errors**: Catches other exceptions, prints the error, and returns a general error message.
- **404 Error**: Custom 404 error page is served when a route is not found.

### Commented Out Features

- **File Upload and Batch Insert**: The commented-out code shows intent for features such as uploading CSV files to tables and performing batch inserts with validation and error handling.

### Docker Setup

- The application is designed to be run inside a Docker container. It listens on all network interfaces (`0.0.0.0`) to be accessible from outside the container.

## Technical Details

- **Configuration**: Database connection settings are managed through environment variables, making the application flexible and secure.
- **SQL Queries**: SQL queries are used to retrieve and aggregate data, with joins and aggregations performed directly in the queries.
- **Error Handling**: Basic error handling is implemented for database connection issues and other exceptions.
- **Flask Routing**: The application defines routes to handle various endpoints and return the appropriate JSON responses.
