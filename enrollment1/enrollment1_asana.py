import asana
from asana.rest import ApiException
from pprint import pprint



configuration = asana.Configuration()
configuration.access_token = 'ACCESS_TOKEN'
api_client = asana.ApiClient(configuration)
