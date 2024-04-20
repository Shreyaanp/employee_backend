from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import pool
import logging
import os
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)


logging.basicConfig(filename='api_database_operations.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')


def initialize_database():
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(100),
                position VARCHAR(100),
                salary DECIMAL
            );
        """)
        conn.commit()
    conn.close()


def setup_connection_pool():
    try:
        db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
        if db_pool:
            logging.info("Connection pool created successfully")
        return db_pool
    except psycopg2.DatabaseError as e:
        logging.error("Error in creating connection pool: %s", e)
        raise

db_pool = setup_connection_pool()

class EmployeeSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    department = fields.Str(required=True)
    position = fields.Str(required=True)
    salary = fields.Float(required=True, validate=validate.Range(min=0))

@app.route('/employees', methods=['GET'])
def get_employees():
    with db_pool.getconn() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM employees;")
                results = cursor.fetchall()
                employees = [{'id': row[0], 'name': row[1], 'department': row[2], 'position': row[3], 'salary': row[4]} for row in results]
                return jsonify(employees), 200
        finally:
            db_pool.putconn(conn)

@app.route('/employee', methods=['POST'])
def add_employee():
    try:
        data = EmployeeSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    with db_pool.getconn() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO employees (name, department, position, salary) VALUES (%s, %s, %s, %s) RETURNING id;",
                               (data['name'], data['department'], data['position'], data['salary']))
                employee_id = cursor.fetchone()[0]
                conn.commit()
                return jsonify({'message': 'Employee added', 'employee_id': employee_id}), 201
        finally:
            db_pool.putconn(conn)

@app.route('/employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = EmployeeSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    with db_pool.getconn() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE employees SET name=%s, department=%s, position=%s, salary=%s WHERE id=%s RETURNING id;",
                               (data['name'], data['department'], data['position'], data['salary'], employee_id))
                if cursor.rowcount == 0:
                    return jsonify({'error': 'Employee not found'}), 404
                conn.commit()
                return jsonify({'message': 'Employee updated', 'employee_id': employee_id}), 200
        finally:
            db_pool.putconn(conn)

@app.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    with db_pool.getconn() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM employees WHERE id=%s RETURNING id;", (employee_id,))
                if cursor.rowcount == 0:
                    return jsonify({'error': 'Employee not found'}), 404
                conn.commit()
                return jsonify({'message': 'Employee deleted'}), 200
        finally:
            db_pool.putconn(conn)

if __name__ == '__main__':
    initialize_database() 
    app.run(debug=True)
