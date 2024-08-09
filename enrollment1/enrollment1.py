import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests
from helpers import get_gid_from_json



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
    
    
opts = {
    'opt_fields': "name,created_at,completed,completed_at,due_at,f'https://app.asana.com/api/1.0/projects/{project_gid}/tasks'", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}

try:
    # Get tasks from a project
    api_response = tasks_api_instance.get_tasks_for_project(project_gid, opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling TasksApi->get_tasks_for_project: %s\n" % e)