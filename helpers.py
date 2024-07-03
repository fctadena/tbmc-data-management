import os
import pandas as pd

def list_files_in_folder(folder_name):
    """
    List all files in the specified folder.
    
    Args:
    - folder_name (str): Name of the folder to scan.
    
    Returns:
    - list: List of filenames in the folder.
    """
    # Initialize an empty list to store filenames
    file_list = []
    
    # Check if the folder exists
    if os.path.exists(folder_name):
        # Iterate through all files in the folder
        for filename in os.listdir(folder_name):
            # Check if it's a file (not a subdirectory)
            if os.path.isfile(os.path.join(folder_name, filename)):
                # Add the filename to the list
                file_list.append(filename)
    else:
        print(f"Folder '{folder_name}' does not exist.")
    
    return file_list

# Example usage:
folder_name = 'data\quotation_princing_analysis'  # Replace with your folder path
files = list_files_in_folder(folder_name)
print("Files in folder:", files)




def planner_task(data):
    pass

def transformer_mimi(filename):
    try:
        data = pd.read_excel(filename)
        return data
    except Exception as e:
        print("Error occurred while opening the Excel file:", str(e))

# # Example usage
# filename = "example.xlsx"
# data = open_excel_file(filename)
# print(data.head())



def transform_dataframe(df):
    new_records = []
    for index, row in df.iterrows():
        assigned_to = row['assigned_to'].split(';')
        for name in assigned_to:
            new_record = {'task': row['task'], 'assigned_to': name}
            new_records.append(new_record)
    new_df = pd.DataFrame(new_records)
    return new_df

# Example usage
df = pd.DataFrame({'task': ['Task 1'], 'assigned_to': ['Assignee1;Assignee2']})
transformed_df = transform_dataframe(df)
print(transformed_df)