import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'base.sqlite3'),
    }
}

# psycopg2

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'base',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True
    }
}

# mysqlclient

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# pyodbc

SQLSERVER = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'base',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    },
}
