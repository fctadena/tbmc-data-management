import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text


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

# db_params = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'database': os.getenv('DB_NAME', 'tbmc_db'),
#     'user': os.getenv('DB_USER', 'tbmc_db_user'),
#     'password': os.getenv('DB_PASSWORD', 123456),
#     'table': os.getenv('DB_TABLE', 'tbmc_db1')
# }


db_params = {
    'host':'localhost',
    'database':'tbmc_db',
    'user': 'tbmc_db_user',
    'password': 123456,
    'table':'tbmc_db1'
    }


def connection_config():
    try:
        # Creating connection to the Postgres server
        conn = psycopg2.connect(
            host=db_params['host'],
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password']
        )
        # Setting automatic commit to True
        conn.set_session(autocommit=True)
        
        # Creating engine for SQLAlchemy
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:5432/{db_params['database']}")
        
        return conn, engine
    
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None


def file_readiness_checker():
    # Check if the file exists
    print("Checking if 'Envelope Recipient Report.csv' exists")
    if not os.path.exists("Envelope Recipient Report.csv"):
        print("File does not exist. Exiting..")
        return None

    print("'Envelope Recipient Report.csv' exists. Proceeding to read file...")
    try:
        data = pd.read_csv("Envelope Recipient Report.csv")
        print("Successfully read file")
    except Exception as e:
        print(f"Error while reading file: {e}")
        return None

    # Check if columns match expected columns
    actual_columns = [col.replace("\ufeff", "") for col in data.columns]
    if actual_columns == expected_columns:
        print("Columns are OK")
        return data
    else:
        print("Columns are not OK")
        return None




def data_upload(data, engine):
    with engine.connect() as conn:
        table_name = db_params['table']
        csv_file = "Envelope Recipient Report.csv"

        try:
            # Check if the table exists
            if conn.dialect.has_table(conn, table_name):
                # Drop the table with CASCADE
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                print(f"Table '{table_name}' dropped successfully (including dependent objects).")
            else:
                print(f"Table '{table_name}' does not exist. Proceeding to create a new table.")

            # Create a new table and upload the data
            data.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Data from '{csv_file}' uploaded successfully to table '{table_name}'.")

        except Exception as e:
            print(f"Error uploading data from '{csv_file}' to table '{table_name}': {e}")
            


# if __name__ == "__main__":
#     data = file_readiness_checker()
#     if data is not None:
#         conn, engine = connection_config()
#         if conn and engine:
#             data_upload(data, engine)
#             conn.close()
            
            
if __name__ == "__main__":
    try:
        data = file_readiness_checker()
        if data is not None:
            conn, engine = connection_config()
            if conn and engine:
                data_upload(data, engine)
                conn.close()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        
        
#### NOT WORKING!!!!