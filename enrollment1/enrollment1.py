import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
from helpers import get_gid_from_json
import pandas as pd
from datetime import datetime


gid_file_path = 'workspace.json'

load_dotenv()
access_token = os.getenv('ASANA_TOKEN')
# workspace_gid = get_gid_from_json(gid_file_path)
workspace_gid = "1207998439135084"



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
def extract_assignee_name(assignee_dict):
    if assignee_dict is None:
        return "<unassigned>"
    else:
        email = assignee_dict['name']
        first_name, last_name = email.split('@')[0].split('.')
        return f"{first_name.capitalize()} {last_name.capitalize()}"

# Apply the function to the 'assignee' column
df['PIC'] = df['PIC'].apply(lambda x: extract_assignee_name(x) if x else "<unassigned>")

def extract_date(timestamp):
    if pd.isna(timestamp) or timestamp == '':
        return ''
    return timestamp.split('T')[0]

# Apply the function to the 'created_at' column
df['INIT DATE'] = df['INIT DATE'].apply(lambda x: extract_date(x))

def extract_membership_name(memberships):
    try:
        if memberships and isinstance(memberships, list):
            if len(memberships) > 0 and isinstance(memberships[0], dict):
                return memberships[0].get('section', {}).get('name', '')
        return ''
    except Exception as e:
        print(f"Error processing memberships: {e}")
        return ''

# Apply the function to the 'memberships' column
df['STATUS'] = df['STATUS'].apply(lambda x: extract_membership_name(x))

def extract_names(tag_list):
    if not tag_list:
        return []
    return [tag['name'] for tag in tag_list]

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

def determine_task_type(tags):
    if 'TARGET' in tags:
        return 'TARGET'
    elif 'ADDITIONAL' in tags:
        return 'ADDITIONAL'
    else:
        return '<no_type>'

df['TYPE'] = df['tags'].apply(lambda x: determine_task_type(x))

def determine_doc_type(tags):
    if 'MPLAN' in tags:
        return 'MPLAN'
    elif 'AMM' in tags:
        return 'AMM'
    else:
        return '<no_doc_type>'

df['DOC_TYPE'] = df['tags'].apply(lambda x: determine_doc_type(x))


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
    "PEC 2020: Spot Cooling",
    "<X> VACUUM PUMP"
]


def find_project(tags):
    for project in project_list:
        if project in tags:
            return project
    return None

df['PROJECT'] = df['tags'].apply(lambda x: find_project(x))

def calculate_age(init_date_str):
    init_date = pd.to_datetime(init_date_str)
    today = datetime.now()
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




# Function to calculate the age in days
def calculate_age_in_days(timestamp):
    if pd.isna(timestamp):
        return None
    # Convert string to datetime object
    timestamp_date = datetime.strptime(timestamp, '%Y-%m-%d').date()
    return (datetime.now().date() - timestamp_date).days

# Applying the function to create a new column 'AGE (DAYS)'
df['AGE (DAYS)'] = df['TIMESTAMP'].apply(lambda x: calculate_age_in_days(x))



print(df)





