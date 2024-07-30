# Data Integration POC

## Objective
Create a Proof of Concept (POC) for a data integration API solution similar to Airbyte. The POC should demonstrate the ability to extract data from a source, transform it, and load it into a destination.

## Requirements
- Python 3.8+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Passlib
- JWT
- Uvicorn
- Requests
- Motor (Async MongoDB driver)
- SQLModel

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/RajeshChoudharytech/data_integration_poc.git
    cd data_integration_poc
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the project:
    ```bash
    uvicorn app.main:app --reload
    ```

4. Check if the project is running:
    Open your browser and navigate to:
    ```bash
    http://localhost:8000/health-check
    ```

## Endpoints

### User Signup
- **URL**: `localhost:8000/v1/user`
- **Method**: POST
- **Body**:
    ```json
    {
      "username": "test name",
      "first_name": "test",
      "last_name": "lastname",
      "password": "testpassword1"
    }
    ```

### User Login
- **URL**: `localhost:8000/v1/user/login`
- **Method**: POST
- **Body**:
    ```json
    {
      "username": "test name",
      "password": "testpassword1"
    }
    ```

### Register Source
- **URL**: `localhost:8000/v1/source`
- **Method**: POST
- **Body**:
    ```json
    {
      "url": "https://jsonplaceholder.typicode.com/posts"
    }
    ```

### Sync and Transform Source
- **URL**: `localhost:8000/v1/sync?id={source_id}`
- **Method**: POST

### Register Synced Data in Local Database
- **URL**: `localhost:8000/v1/destination?id={source_id}`
- **Method**: POST
