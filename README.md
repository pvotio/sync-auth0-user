# Sync Auth0 Users from SQL Server

This project provides an automated pipeline to synchronize users and their roles from a Microsoft SQL Server database with an Auth0 tenant using the Auth0 Management API. It ensures that users present in the database are accurately reflected in Auth0 and are provisioned with appropriate roles while removing stale or outdated entries.

## Overview

### Purpose

This application is designed to:
- Authenticate with Auth0 using the client credentials flow.
- Retrieve user records from a SQL Server database.
- Compare and reconcile user records with existing Auth0 users.
- Add new users to Auth0.
- Remove users from Auth0 that no longer exist in the database.
- Update user roles to align with roles defined in the SQL system.

This synchronization process enables centralized user lifecycle management across identity providers and internal systems.

## Source of Data

- **Database**: User records (email, role) are retrieved from a table defined by `USERS_DB_QUERY`.
- **Auth0**: Users and roles are managed via the Auth0 Management API (`/api/v2/`), using:
  - `/users`
  - `/roles`
  - `/users/{id}/roles`

## Application Flow

The logic is orchestrated in `main.py`, invoking the `App` class, which performs the following:

1. **Initialization**:
   - Database connection is established.
   - Auth0 client is initialized and tokenized.
   - Users and roles are fetched from both data sources.

2. **Comparison and Sync**:
   - **Add Users**: New database users are added to Auth0 and assigned appropriate roles.
   - **Delete Users**: Auth0 users not found in the database (except for those in an ignore list) are deleted.
   - **Update Roles**: Existing users have their roles reassigned if mismatches are detected.

3. **Parallelization**:
   - Multiprocessing is used to retrieve user roles from Auth0 in parallel, improving performance for large user bases.

## Project Structure

```
sync-auth0-user-main/
├── client/                # Auth0 interaction and orchestration
│   ├── app.py             # User sync logic
│   └── auth0.py           # Auth0 API client
├── config/                # Logging and environment settings
├── database/              # MSSQL integration
├── main.py                # Application entrypoint
├── .env.sample            # Sample environment configuration
├── Dockerfile             # Container configuration
```

## Environment Variables

Create a `.env` file based on `.env.sample`. Important variables include:

| Variable | Description |
|----------|-------------|
| `USERS_DB_QUERY` | SQL query used to fetch users from MSSQL |
| `AUTH0_URL` | Auth0 domain URL (e.g., `https://your-tenant.auth0.com`) |
| `AUTH0_CLIENT_ID` / `AUTH0_CLIENT_SECRET` | Auth0 API credentials |
| `AUTH0_CONNECTION` | Name of Auth0 connection for user creation |
| `CLIENT_IGNORE_USERS` | Comma-separated list of emails to ignore from deletion |
| `MSSQL_*` | Server, database, and authentication details |
| `AUTH0_MAX_RETRIES`, `AUTH0_BACKOFF_FACTOR` | Retry behavior for rate-limited requests |

## Docker Support

The project can be containerized using the provided Dockerfile.

### Build the Image
```bash
docker build -t sync-auth0-users .
```

### Run the Container
```bash
docker run --env-file .env sync-auth0-users
```

## Requirements

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

Libraries used include:
- `requests` for HTTP communication
- `pandas` for user record handling
- `pyodbc` and `SQLAlchemy` for MSSQL
- `multiprocessing` for parallel API queries

## Running the App

After setting your `.env`, simply run:

```bash
python main.py
```

The script logs each user processed, including:
- Users added to Auth0
- Users deleted from Auth0
- Role updates and assignments

## License

This project is licensed under the MIT License. Auth0 usage is subject to your service-level agreement with Auth0 and compliance with their API rate limits and data policies.
