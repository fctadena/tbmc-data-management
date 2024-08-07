import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
import requests

load_dotenv()
access_token = os.getenv('ASANAPLANNER1_TOKEN')
workspace_gid = os.getenv('GID')

configuration = asana.Configuration()
configuration.access_token = access_token
api_client = asana.ApiClient(configuration)

#APP 1: BASIC OVERVIEW

#PART 1: GETTING RAW DATA
#1.1 SET AUTHRORIZATION
#1.2 GET REQUIRED PARAMS (WORKSPACE, PROJECT, ETC)
#1.3 SETUP FUNCTION TO CALL THE API FOR ALL TASK IN THE PROJECT AND RETURN A DATAFRAME FOR FURTHER PROCESSING.

#PART 2: TRANSFORMING THE RAW DATA
#2.1 SET
#2.2
#2.3 




#APP 2: 


# create an instance of the API class
tasks_api_instance = asana.TasksApi(api_client)
opts = {
    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
    'project': "321654", # str | The project to filter tasks on.
    'section': "321654", # str | The section to filter tasks on.
    'workspace': "321654", # str | The workspace to filter tasks on. *Note: If you specify `workspace`, you must also specify the `assignee` to filter on.*
    'completed_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that are either incomplete or that have been completed since this time.
    'modified_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that have been modified since the given time.  *Note: A task is considered “modified” if any of its properties change, or associations between it and other objects are modified (e.g.  a task being added to a project). A task is not considered modified just because another object it is associated with (e.g. a subtask) is modified. Actions that count as modifying the task include assigning, renaming, completing, and adding stories.*
    'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}

try:
    # Get multiple tasks
    api_response = tasks_api_instance.get_tasks(opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling TasksApi->get_tasks: %s\n" % e)