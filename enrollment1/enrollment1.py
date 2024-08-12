import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
# from helpers import get_gid_from_json
import pandas as pd
from datetime import datetime
import json


# def get_gid_from_json(file_path):
#     # Open and read the JSON file
#     with open(file_path, 'r') as file:
#         data = json.load(file)
    
#     # Extract the value of gid
#     gid = data['data'][0]['gid']
#     return gid


def get_gid_from_json():
    gid = "1207998439135084"
    return gid



# gid_file_path = 'workspace.json'

load_dotenv()
access_token = os.getenv('ASANA_TOKEN')
workspace_gid = get_gid_from_json()




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


# # Function to extract the name from the email or handle None/empty cases
# def extract_name(assignee_dict):
#     if assignee_dict is None:
#         return "<unassigned>"
    
#     else:
#         email = assignee_dict['name']
#         first_name, last_name = email.split('@')[0].split('.')
#         return f"{first_name.capitalize()} {last_name.capitalize()}"

def extract_name(assignee_dict):
    if assignee_dict is None:
        return ""
    else:
        email = assignee_dict.get('name')
        if email is None:
            return ""
        else:
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


print(df)