
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text, MetaData, Table
from dotenv import load_dotenv, dotenv_values


load_dotenv()


expected_columns = [
    '"Envelope ID"',
    'Subject',
    'Status',
    'Sender Name',
    'Recipient Name',
    'Routing Order',
    'Action',
    'Sent On (Date)',
    'Sent On (Time)',
    'Completed On (Date)',
    'Completed On (Time)',
    'Completion Time (DD:HH:MM)'
]


db_params = {
    'host': os.getenv('DB_HOST') or 'localhost',
    'database': os.getenv('DB_NAME') or 'tbmc_db',
    'user': os.getenv('DB_USER') or 'tbmc_db_user',
    'password': os.getenv('DB_PASSWORD') or '123456',
    'table': os.getenv('DB_TABLE') or 'tbmc_db1'
}



def check_file_and_columns(file_path):
    print(f"Checking if '{file_path}' exists")
    if not os.path.exists(file_path):
        print("File does not exist. Exiting..")
        return None
    
    print(f"'{file_path}' exists. Proceeding to read file...")
    try:
        data = pd.read_csv(file_path)
        print("Successfully read file")
        actual_columns = [col.replace("\ufeff", "") for col in data.columns]
        if actual_columns == expected_columns:
            print("Columns are correct")
            return data
        else:
            print("Columns are not OK")
            return None
    except Exception as e:
        print(f"Error while reading file: {e}")
        return None

def connect_to_database(db_params):
    try:
        conn = psycopg2.connect(
            host=db_params['host'],
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password']
        )
        conn.set_session(autocommit=True)
        
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:5432/{db_params['database']}")
        
        print("Database connection successful")
        return conn, engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None

def upload_to_database(data, engine, table_name):
    try:
        # Drop table if exists
        meta = MetaData()
        meta.reflect(bind=engine)
        
        if table_name in meta.tables:
            meta.tables[table_name].drop(engine, checkfirst=True)
            print(f"Table '{table_name}' dropped successfully (including dependent objects).")
        else:
            print(f"Table '{table_name}' does not exist. Proceeding to create a new table.")
        
        # Upload data to database
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data uploaded successfully to table '{table_name}'.")
    except Exception as e:
        print(f"Error uploading data to database: {e}")

if __name__ == "__main__":
    file_path = "Envelope Recipient Report.csv"
    
    print(f"Checking file '{file_path}' and verifying columns...")
    data = check_file_and_columns(file_path)
    
    if data is not None:
        print("File check successful.")
        print("Connecting to database...")
        conn, engine = connect_to_database(db_params)
        
        if conn and engine:
            print("Database connection successful.")
            table_name = db_params['table']
            
            print(f"Uploading data to table '{table_name}'...")
            upload_to_database(data, engine, table_name)
            
            conn.close()
            print("Database connection closed.")
            
    else:
        print("File check failed or columns are incorrect. Exiting.")
