# Employee Manager API

The Employee Manager API is a Flask-based web service designed to manage employee records in a PostgreSQL database. It provides endpoints for creating, retrieving, updating, and deleting employee records efficiently, utilizing a connection pool for database interactions.

## Features

- **CRUD Operations**: Create, read, update, and delete employee records.
- **Connection Pooling**: Efficient management of database connections.
- **Data Validation**: Ensures the integrity of incoming data using Marshmallow.
- **Secure Configuration**: Utilizes environment variables for configuration to enhance security.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **PostgreSQL**: An open source object-relational database system.
- **Psycopg2**: PostgreSQL database adapter for Python.
- **Marshmallow**: An ORM/ODM/framework-agnostic library for complex data types serialization and deserialization.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.8+
- PostgreSQL
- pipenv or virtual environment manager

### Installing

A step by step series of examples that tell you how to get a development environment running:

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/employee-manager-api.git
   cd employee-manager-api
   ```
2. **Setup a virtual environment**

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   ```bash
   Copy the .env.example file to .env and modify it to include your database credentials and other configurations.
   ```

5. **Initialize the database**

   ```bash
   python
    >>> from main import initialize_database
    >>> initialize_database()

   ```

6. **Run the server**

   ```bash
   flask run
   ```
## Environment Variables

Make sure to set these variables in your `.env` file:

- `DATABASE`: Name of your PostgreSQL database
- `USER`: Database user
- `PASSWORD`: Database password
- `HOST`: Hostname, typically `localhost`

## API Endpoints

| Method | URL                | Action                                  |
|--------|--------------------|-----------------------------------------|
| GET    | `/employees`       | Retrieves a list of all employees       |
| POST   | `/employee`        | Adds a new employee                     |
| PUT    | `/employee/{id}`   | Updates an existing employee's details  |
| DELETE | `/employee/{id}`   | Deletes an employee                     |

