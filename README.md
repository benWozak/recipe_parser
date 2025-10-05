# Recipe Parser API (Early Prototype)

This is an early prototype/proof of concept for what eventually became [HomeChef Companion](https://github.com/benWozak/homechef-companion-frontend). The project was built to test the feasibility of parsing recipes from various sources, particularly Instagram posts.

## Features

- Instagram recipe post parsing
- User authentication via Auth0
- Household management for shared recipes
- Recipe storage and management
- PostgreSQL database with SQLAlchemy ORM
- FastAPI backend framework

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: Auth0
- **Migration Tool**: Alembic
- **Python Dependencies**: See requirements.txt

## Local Development

1. Create a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_AUDIENCE=your-api-audience
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
```

4. Run database migrations:

```sh
alembic upgrade head
```

5. Start the development server:

```sh
uvicorn app.main:app --reload
```

## Note

This project served as a prototype for exploring recipe parsing capabilities and establishing a basic API structure. For the current version of this application, please visit [HomeChef Companion](https://github.com/benWozak/homechef-companion-frontend).
