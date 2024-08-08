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
            return data['gid']
            # pprint(data)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspaces: %s\n" % e)
        
        
# workspace_gid = get_workspace_gid(opts_workspaces)
# print(workspace_gid)


# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)
workspace_gid = get_workspace_gid(opts_workspaces) # str | Globally unique identifier for the workspace or organization.
opts_workspace_projects = {
    # 'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
    # 'offset': "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*
    # 'archived': False, # bool | Only return projects whose `archived` field takes on the value of this parameter.
    'opt_fields': f"https://app.asana.com/api/1.0/workspaces/{workspace_gid}/projects", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}

def get_workspace_projects(opts_workspace_projects):
    try:
        # Get all projects in a workspace
        api_response = projects_api_instance.get_projects_for_workspace(workspace_gid, opts_workspace_projects)
        for data in api_response:
            pprint(data)
    except ApiException as e:
        print("Exception when calling ProjectsApi->get_projects_for_workspace: %s\n" % e)

get_workspace_projects = get_workspace_projects(opts_workspace_projects)
print(opts_workspace_projects)