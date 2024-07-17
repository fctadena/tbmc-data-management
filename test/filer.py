import os

def scan_folder(target_folder):
    file_list = []
    folder_list = []
    
    # Check if the target folder exists
    if not os.path.exists(target_folder):
        print("Target folder does not exist.")
        return []
    
    # Scan through the target folder
    for item in os.listdir(target_folder):
        item_path = os.path.join(target_folder, item)
        if os.path.isfile(item_path):
            file_list.append(item)
        elif os.path.isdir(item_path):
            folder_list.append(item)
    
    return file_list + folder_list



folder_path = "C:\Users\PHTadenaFr\Documents\scripts"
result = scan_folder(folder_path)
print(result)