# Online Shop API

Backend API for the Online Shop application, built with FastAPI.

## Prerequisites

- **Python**: 3.8+
- **Database**: MySQL (or compatible)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd online_shop
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables:**
    Copy the example environment file to create your local configuration:

    ```bash
    cp env.example .env
    ```

2.  **Edit `.env`:**
    Open `.env` and configure your database credentials and security settings:

    ```ini
    # Security
    SECRET_KEY=your_secure_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    # Database
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_db_password
    DB_NAME=db_inventories
    ```

## Database Setup

1.  **Initialize Database:**
    Ensure your MySQL server is running and the database `db_inventories` exists (or whatever you named it in `.env`).

2.  **Run Migrations:**
    Apply the database schema using Alembic:
    ```bash
    alembic upgrade head
    ```

## Running the Application

Start the development server:

```bash
uvicorn api.main:api --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## Documentation

- **Interactive API Docs**: Go to [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI) or [http://localhost:8000/redoc](http://localhost:8000/redoc).
- **API Specification**: See [api_specs.md](./api_specs.md) for detailed endpoint documentation.
