import os

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
