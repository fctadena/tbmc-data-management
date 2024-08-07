#USE ASANA TO MANAGE THE ENROLLMENT AND GENERATE DASHBOARD USING THE API FOR THE FREE TIER
import requests
import pandas as pd

def authenticate():
    # Set the authentication header
    headers = {
        "Authorization": "Bearer "
    }
    return headers

def fetch_data(auth_headers):
    # Set the endpoint URL
    endpoint_url = "https://example.com/api/endpoint"

    try:
        # Send a GET request to the endpoint with the authentication header
        response = requests.get(endpoint_url, headers=auth_headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the JSON data from the response
            json_data = response.json()

            return json_data
        else:
            print("Error: Request failed with status code", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error: Request failed -", str(e))
        return None

def transform_data(json_data):
    # Perform data transformation operations on the JSON data
    # For example, convert specific fields, filter rows, etc.
    transformed_data = json_data

    # Create a Pandas dataframe from the transformed data
    dataframe = pd.DataFrame(transformed_data)

    return dataframe

def main():
    # Authenticate
    auth_headers = authenticate()

    # Fetch data
    json_data = fetch_data(auth_headers)

    if json_data:
        # Transform data
        transformed_dataframe = transform_data(json_data)

        # Print the transformed dataframe
        print(transformed_dataframe)

        # Return the transformed dataframe
        return transformed_dataframe
    else:
        return None

if __name__ == "__main__":
    main()