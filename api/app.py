from flask import Flask
import mysql.connector
from config import config
import pandas as pd
import os
app = Flask(__name__)

# Access environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

config = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port,
    'database': db_name
}

@app.route('/jobs')
def jobs():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        sql = """SELECT * FROM jobs"""
        cursor.execute(sql)
        data = cursor.fetchall()
        lst_jobs = []
        for row in data:
            job = {'id':row[0],'job':row[1]}
            lst_jobs.append(job)
        return lst_jobs
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Database connection failed: {err}"
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return f"An unexpected error occurred: {ex}"

@app.route('/hired_employees_2021_quarters')
def hired_employees_2021_quarters():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        sql = """SELECT 
                    department,
                    job,
                    COUNT(CASE WHEN entry_quarter = 1 THEN 1 END) AS Q1,
                    COUNT(CASE WHEN entry_quarter = 2 THEN 1 END) AS Q2,
                    COUNT(CASE WHEN entry_quarter = 3 THEN 1 END) AS Q3,
                    COUNT(CASE WHEN entry_quarter = 4 THEN 1 END) AS Q4
                FROM (
                    SELECT
                        hired_employees.id as id,
                        hired_employees.employee as employee,
                        YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_year,
                        MONTH(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_month,
                        QUARTER(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_quarter,
                        hired_employees.department_id as department_id,
                        hired_employees.job_id as job_id,
                        departments.department as department,
                        jobs.job as job
                    FROM hired_employees 
                    LEFT JOIN departments
                    ON departments.id = hired_employees.department_id
                    LEFT JOIN jobs
                    ON jobs.id = hired_employees.job_id
                ) AS subquery
                WHERE entry_year = 2021
                GROUP BY job, department
                ORDER BY count(id) DESC"""
        cursor.execute(sql)
        data = cursor.fetchall()
        lst_jobs = []
        for row in data:
            job = {'department':row[0],'job':row[1],'Q1':row[2],'Q2':row[3],'Q3':row[4],'Q4':row[5]}
            lst_jobs.append(job)
        return lst_jobs
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Database connection failed: {err}"
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return f"An unexpected error occurred: {ex}"
    
@app.route('/hired_employees_2021')
def hired_employees_2021():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        sql = """   SELECT
                        id,
                        department,
                        hired
                    FROM (
                        SELECT
                            id,
                            department,
                            count(employee) as hired
                        FROM (
                            SELECT
                                departments.id as id,
                                departments.department as department,
                                hired_employees.employee,
                                YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_year,
                                QUARTER(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_quarter
                            FROM departments
                            LEFT JOIN hired_employees
                            ON departments.id = hired_employees.department_id) AS subquery
                            WHERE entry_year = 2021
                            GROUP BY id, department
                        ) AS subquery2
                    WHERE hired > (
                        SELECT 
                            AVG(hired)
                        FROM (
                                SELECT
                                    departments.id as id,
                                    departments.department as department,
                                    count(hired_employees.employee) as hired
                                FROM departments
                                LEFT JOIN hired_employees
                                ON departments.id = hired_employees.department_id
                                WHERE YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) = 2021
                                GROUP BY id, department
                                ) AS subquery
                            )
                    ORDER BY hired DESC"""
        cursor.execute(sql)
        data = cursor.fetchall()
        lst_hirings = []
        for row in data:
            job = {'id':row[0],'department':row[1],'hired':row[2]}
            lst_hirings.append(job)
        return lst_hirings
    except Exception as ex: 
        return "Error"

#@app.route('/upload/<table_name>', methods=['POST'])
#def upload_file(table_name):
#    if 'file' not in request.files:
#        return jsonify({"error": "No file part"}), 400
#    file = request.files['file']
#    if file.filename == '':
#        return jsonify({"error": "No selected file"}), 400
#
#    if table_name not in ['departments', 'jobs', 'employees']:
#        return jsonify({"error": "Invalid table name"}), 400
#
#    df = pd.read_csv(file)
#    try:
#        if table_name == 'departments':
#            df.to_sql('department', conexion, if_exists='append', index=False)
#        elif table_name == 'job':
#            df.to_sql('jobs', conexion, if_exists='append', index=False)
#        elif table_name == 'employees':
#            df.to_sql('employee', conexion, if_exists='append', index=False)
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500
#
#    return jsonify({"message": f"Data uploaded to {table_name} successfully"}), 201
#
#@app.route('/batch_insert/<table_name>', methods=['POST'])
#def batch_insert(table_name):
#    data = request.json
#    if not data or len(data) > 1000:
#        return jsonify({"error": "Invalid data or too many rows (max 1000)"}), 400
#
#    try:
#        if table_name == 'departments':
#            conexion.session.bulk_insert_mappings(Department, data)
#        elif table_name == 'job':
#            conexion.session.bulk_insert_mappings(Job, data)
#        elif table_name == 'employees':
#            conexion.session.bulk_insert_mappings(Employee, data)
#        conexion.session.commit()
#    except Exception as e:
#        db.session.rollback()
#        return jsonify({"error": str(e)}), 500
#
#    return jsonify({"message": f"Batch insert to {table_name} successful"}), 201
#
#@app.route('/upload-csv', methods=['POST'])
#def upload_csv():
#    if 'file' not in request.files:
#        return jsonify({"error": "No file part in the request"}), 400
#
#    file = request.files['file']
#
#    if file.filename == '':
#        return jsonify({"error": "No selected file"}), 400
#
#    if file and file.filename.endswith('.csv'):
#        try:
#            # Use pandas to read the CSV file
#            data = pd.read_csv(file)
#            # Process your CSV data as needed
#            return jsonify({"message": "File successfully uploaded and processed"}), 200
#        except Exception as e:
#            return jsonify({"error": str(e)}), 500
#
#    return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

def page_not_found(error):
    return "<h1> Your desired paged doesn't exist... </h1>"

if __name__ == '__main__':
    #app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run(host='0.0.0.0')