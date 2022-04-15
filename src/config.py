import os

user = os.environ.get('DB_USER', 'postgres')
password = os.environ.get('DB_PASSWORD', 'postgres')
host = os.environ.get('DB_HOST', 'localhost')
database = os.environ.get('DB', 'postgres')
port = 5432

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'