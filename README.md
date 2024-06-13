# FastAPI Project

This is a bitA test project that integrates with PostgreSQL for data storage and uses Selenium for web crawling to retrieve data from websites.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- PostgreSQL
- SQLAlchemy
- Selenium

## Installation

1. Install the dependencies: pip install -r requirements.txt
2. Set up the PostgreSQL database:
   
   - Create a PostgreSQL database.
   - Update the database connection string in `config.py` with your database credentials.
## Usage

1. Start the FastAPI server using Uvicorn:
2. Open your web browser and go to `http://localhost:8000/docs` to access the Swagger UI. Here, you can interact with the API endpoints and view the documentation.

3. Use the API endpoints to perform CRUD operations on the data stored in PostgreSQL.

4. To use the web crawling functionality:
   
   - Run `app/crawl/crawl_data.py` file using Selenium.

## API Endpoints

- `/products`: CRUD operations for items stored in the PostgreSQL database.
