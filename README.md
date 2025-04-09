# PingCRM Backend

This is the backend for the PingCRM application, built with FastAPI, SQLAlchemy, and PostgreSQL. It provides APIs for managing organizations and contacts.

## Features
- CRUD operations for organizations and contacts
- Search and filter functionality for contacts
- PostgreSQL database integration
- Environment-based configuration for security

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Environment Management**: python-dotenv

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database (e.g., Supabase or local instance)

### Installation
1. Clone the repository:
  git clone https://github.com/yourusername/pingcrm-backend.git
  cd pingcrm-backend

  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt

2. Create a .env file in the root directory.
   Add your database URL: DATABASE_URL=postgresql://user:password@host:port/dbname

3. Run the application: uvicorn main:app --reload
