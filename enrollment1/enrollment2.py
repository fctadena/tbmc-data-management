import asana
from asana.rest import ApiException
from pprint import pprint
import os
import requests
from helpers import get_gid_from_json
import pandas as pd
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine, text, MetaData, Table
from dotenv import load_dotenv, dotenv_values


gid_file_path = 'workspace.json'

load_dotenv()
access_token = os.getenv('ASANA_TOKEN')
workspace_gid = get_gid_from_json(gid_file_path)




configuration = asana.Configuration()
configuration.access_token = access_token
api_client = asana.ApiClient(configuration)


# create an instance of the API class
workspaces_api_instance = asana.WorkspacesApi(api_client)
opts_workspaces = {
    'opt_fields': "https://app.asana.com/api/1.0/workspaces" # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}


def get_workspace_gid(opts_workspaces):
    try:
        # Get multiple workspaces
        api_response = workspaces_api_instance.get_workspaces(opts_workspaces)
        for data in api_response:
            workspace_gid = int(data['gid'])
            print(f'Workspace GID: {workspace_gid}')
            return workspace_gid
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspaces: %s\n" % e)
        
        
workspace_gid = get_workspace_gid(opts_workspaces)



# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)
opts_project = {
    'workspace': workspace_gid # str | The workspace or organization to filter projects on.
}


def get_project_gid(opts_project):
    try:
        # Get multiple projects
        api_response = projects_api_instance.get_projects(opts_project)
        for data in api_response:
            project_name = data['name']
            project_gid = data['gid']
            
            project_details = {
                'project_name': project_name,
                'project_gid': project_gid
            }
            
            print(f'Project Name: {project_name}')
            print(f'Project GID: {project_gid}')

            return project_details
            
    except ApiException as e:
        print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
        
        
project_details = get_project_gid(opts_project)






# create an instance of the API class
tasks_api_instance = asana.TasksApi(api_client)
project_gid = project_details['project_gid'] # str | Globally unique identifier for the project.
    
    
opts_tasks = {
    'opt_fields': "notes,created_at,memberships.section.name,assignee.name,tags.name,name,created_at,f'https://app.asana.com/api/1.0/projects/{project_gid}/tasks'", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
#     'opt_fields': "assignee.name,section,tags.name,name,f'https://app.asana.com/api/1.0/projects/{project_gid}/tasks'", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.

}


def get_all_task(project_gid, opts_tasks):
    try:
        # Get tasks from a project
        api_response = tasks_api_instance.get_tasks_for_project(project_gid, opts_tasks)
        data_list = []
        for data in api_response:
            data_list.append(data)
        
        df = pd.DataFrame(data_list)
        
        return df
    
    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)
        
df = get_all_task(project_gid, opts_tasks)




def rename_column_names(df):
    column_mapping = {
        'created_at': 'INIT DATE',
        'memberships': 'STATUS',
        'assignee': 'PIC',
        'name': 'DESCRIPTION',
        'notes': 'PART / MPLAN NO.'
    }
    df = df.rename(columns=column_mapping)
    return df



df = rename_column_names(df)


# Function to extract the name from the email or handle None/empty cases
def extract_name(assignee_dict):
    if assignee_dict is None:
        return "<unassigned>"
    else:
        email = assignee_dict['name']
        first_name, last_name = email.split('@')[0].split('.')
        return f"{first_name.capitalize()} {last_name.capitalize()}"

# Apply the function to the 'assignee' column
df['PIC'] = df['PIC'].apply(lambda x: extract_name(x) if x else "<unassigned>")

def extract_date(timestamp):
    if pd.isna(timestamp) or timestamp == '':
        return ''
    return timestamp.split('T')[0]

# Apply the function to the 'created_at' column
# df['created_at'] = df['created_at'].apply(lambda x: extract_date(x))
df['INIT DATE'] = df['INIT DATE'].apply(lambda x: extract_date(x))
df['INIT DATE'] = pd.to_datetime(df['INIT DATE'], errors='coerce')

def extract_name(memberships):
    try:
        if memberships and isinstance(memberships, list):
            # Check if the list has at least one dictionary
            if len(memberships) > 0 and isinstance(memberships[0], dict):
                # Extract 'name' from the first dictionary in the list
                return memberships[0].get('section', {}).get('name', '')
        return ''  # Return empty string if conditions are not met
    except Exception as e:
        print(f"Error processing memberships: {e}")
        return ''  # Return empty string in case of any exception

# Apply the function to the 'memberships' column
df['STATUS'] = df['STATUS'].apply(lambda x: extract_name(x))


def extract_names(tag_list):
    if not tag_list:  # Check if the record is empty or None
        return []
    return [tag['name'] for tag in tag_list]  # Extract the 'name' values

df['tags'] = df['tags'].apply(lambda x: extract_names(x))


def determine_project_type(tags):
    if 'OLD' in tags:
        return 'OLD'
    elif 'NEW' in tags:
        return 'NEW'
    else:
        return '<no_project_type>'

df['PROJECT_TYPE'] = df['tags'].apply(lambda x: determine_project_type(x))


def determine_area_type(tags):
    if 'COFFEE' in tags:
        return 'COFFEE'
    elif 'MILK' in tags:
        return 'MILK'
    else:
        return '<no_area>'

df['AREA'] = df['tags'].apply(lambda x: determine_area_type(x))



def determine_type(tags):
    if 'TARGET' in tags:
        return 'TARGET'
    elif 'ADDITIONAL' in tags:
        return 'ADDITIONAL'
    else:
        return '<no_type>'

df['TYPE'] = df['tags'].apply(lambda x: determine_area_type(x))

def determine_doc_type(tags):
    if 'MPLAN' in tags:
        return 'MPLAN'
    elif 'AMM' in tags:
        return 'AMM'
    else:
        return '<no_doc_type>'

df['DOC_TYPE'] = df['tags'].apply(lambda x: determine_doc_type(x))


def determine_type(tags):
    if 'TARGET' in tags:
        return 'TARGET'
    elif 'ADDITIONAL' in tags:
        return 'ADDITIONAL'
    else:
        return '<no_type>'

df['TYPE'] = df['tags'].apply(lambda x: determine_area_type(x))




project_list = [
    "AUTOCOMPACTOR",
    "HYDRAULIC PROJECT",
    "GCU+",
    "WATER HEATER",
    "GCCD Transport Phase 1",
    "SIR",
    "IPTA VACUUM PUMP",
    "ICIP",
    "GC Van Unloading Facility",
    "PEC 2020: PE Panel Cooling",
    "PEC 2020: Process adaptation",
    "FFE-RARE",
    "PEC 2020: Spot Cooling"
]



# Function to find the project in tags
def find_project(tags):
    for project in project_list:
        if project in tags:
            return project
    return None  # or return an empty string "" if no match is found

# Apply the function to the tags column using lambda
df['PROJECT'] = df['tags'].apply(lambda x: find_project(x))



def calculate_age(init_date_str):
    # Convert the string date to a datetime object
    init_date = pd.to_datetime(init_date_str)
    # Get today's date
    today = datetime.now()
    # Calculate the difference in days
    age_days = (today - init_date).days
    return age_days

df['INIT_AGE (DAYS)'] = df['INIT DATE'].apply(lambda x: calculate_age(x))


def task_stories(row):
    return "Temporary REMARKS"

df['REMARKS'] = df.apply(lambda row: task_stories(row), axis=1)





# Define the get_latest_created_at function
def get_latest_created_at(task_gid, stories_api_instance, opts):
    try:
        # Get stories from a task
        api_response = stories_api_instance.get_stories_for_task(task_gid, opts)

        assigned_time = None
        section_changed_time = None
        added_to_project_time = None

        for data in api_response:
            resource_subtype = data.get('resource_subtype')
            created_at = data.get('created_at')

            if created_at:
                created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ').date()

            if resource_subtype == 'assigned':
                assigned_time = created_at_date
            elif resource_subtype == 'section_changed':
                section_changed_time = created_at_date
            elif resource_subtype == 'added_to_project':
                added_to_project_time = created_at_date

        if assigned_time:
            return assigned_time.strftime('%Y-%m-%d')
        elif section_changed_time:
            return section_changed_time.strftime('%Y-%m-%d')
        elif added_to_project_time:
            return added_to_project_time.strftime('%Y-%m-%d')
        else:
            return None

    except asana.ApiException as e:
        print("Exception when calling StoriesApi->get_stories_for_task: %s\n" % e)
        return None

# Set up Asana API client and StoriesApi instance
stories_api_instance = asana.StoriesApi(api_client)
opts = {
    'opt_fields': "created_at,resource_subtype"
}

# Use lambda function to create the new 'TIMESTAMP' column in the DataFrame
df['TIMESTAMP'] = df['gid'].apply(lambda x: get_latest_created_at(x, stories_api_instance, opts))
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')




# Function to calculate the age in days
def calculate_age_in_days(timestamp):
    if pd.isna(timestamp):
        return None
    # Directly use the date() method if timestamp is a Timestamp object
    timestamp_date = timestamp.date() if isinstance(timestamp, pd.Timestamp) else datetime.strptime(timestamp, '%Y-%m-%d').date()
    return (datetime.now().date() - timestamp_date).days

# Applying the function to create a new column 'AGE (DAYS)'
df['AGE (DAYS)'] = df['TIMESTAMP'].apply(calculate_age_in_days)



#DATA TYPES CONVERSION
columns_to_convert = [
    'PIC', 'STATUS', 'DESCRIPTION', 'PROJECT_TYPE',
    'AREA', 'TYPE', 'DOC_TYPE', 'PROJECT', 'REMARKS'
]

df[columns_to_convert] = df[columns_to_convert].astype(str)
df['gid'] = pd.to_numeric(df['gid'], errors='coerce').astype('Int64')  # Use 'Int64' to handle NaN values

df = df.drop(columns=['tags'])


#POPULATING REMARKS COLUMN
def get_remarks_for_task(task_gid):
    configuration = asana.Configuration()
    configuration.access_token = os.getenv('ASANA_TOKEN')
    api_client = asana.ApiClient(configuration)

    stories_api_instance = asana.StoriesApi(api_client)
    opts = {
        'opt_fields': "created_at,resource_subtype,text,created_by.name"
    }

    relevant_subtypes = {"added_to_project", "section_changed", "assigned", "unassigned", "comment_added"}
    remarks = []

    try:
        # Get stories from a task
        api_response = stories_api_instance.get_stories_for_task(task_gid, opts)
        
        for story in api_response:
            if story.get('resource_subtype') in relevant_subtypes:
                # Extract and format the required information
                created_at = story.get('created_at')[:10]  # Extract date only (YYYY-MM-DD)
                resource_subtype = story.get('resource_subtype')
                text = story.get('text')
                formatted_remark = f"[{created_at}] {resource_subtype}: \"{text}\""
                remarks.append(formatted_remark)
                
        
        # Check if no relevant stories were found
        if not remarks:
            remarks.append("<No Relevant Activity>")

    except ApiException as e:
        print("Exception when calling StoriesApi->get_stories_for_task: %s\n" % e)
        remarks.append("<No Relevant Activity>")

    return "\n".join(remarks)

# Example usage with lambda to populate the REMARKS column in the DataFrame
df['REMARKS'] = df['gid'].apply(lambda gid: get_remarks_for_task(gid))


#SAVING TO DATABASE
db_params = {
    'host': os.getenv('DB_HOST') or 'localhost',
    'database': os.getenv('DB_NAME') or 'tbmc_db',
    'user': os.getenv('DB_USER') or 'tbmc_db_user',
    'password': os.getenv('DB_PASSWORD') or '123456',
    'table': os.getenv('DB_TABLE') or 'tbmc_enrollment',
    'port': os.getenv('DB_PORT') or '5432'
}

def connect_to_database(db_params):
    try:
        conn = psycopg2.connect(
            host=db_params['host'],
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password']
        )
        conn.set_session(autocommit=True)
        
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")
        
        return conn, engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None
    
conn, engine = connect_to_database(db_params)

table_name = db_params['table']


def upload_to_database(df, engine, table_name):
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
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data uploaded successfully to table '{table_name}'.")
    except Exception as e:
        print(f"Error uploading data to database: {e}")
        

upload_to_database(df, engine, table_name)
conn.close()
print("Database connection closed.")

