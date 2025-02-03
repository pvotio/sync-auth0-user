from decouple import config

client_ignore_users_cast = lambda v: [
    x.lower().strip() for x in v.split(",") if x.lower().strip() != ""
]


LOG_LEVEL = config("LOG_LEVEL", default="INFO")
AUTH0_MAX_RETRIES = config("AUTH0_MAX_RETRIES", cast=int, default=3)
AUTH0_BACKOFF_FACTOR = config("AUTH0_BACKOFF_FACTOR", cast=int, default=2)
AUTH0_URL = config("AUTH0_URL")
AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET")
AUTH0_CONNECTION = config("AUTH0_CONNECTION")
CLIENT_IGNORE_USERS = config("CLIENT_IGNORE_USERS", cast=client_ignore_users_cast)
MSSQL_AD_LOGIN = config("MSSQL_AD_LOGIN", cast=bool, default=False)
MSSQL_SERVER = config("MSSQL_SERVER")
MSSQL_DATABASE = config("MSSQL_DATABASE")

if not MSSQL_AD_LOGIN:
    MSSQL_USERNAME = config("MSSQL_USERNAME")
    MSSQL_PASSWORD = config("MSSQL_PASSWORD")
