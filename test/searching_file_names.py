import os

def get_excel_files(folder_path):
    excel_files = []
    for file_name in os.listdir(folder_path):
        print(file_name)
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            excel_files.append(file_name)
            parts = file_name.split(" - ")
            if len(parts) == 2:
                print(f"The file name is '{parts[0]}', from '{parts[1]}'.")
            else:
                print("Check file name. Not in format.")
    return excel_files

folder_path = "./test_data"
excel_files = get_excel_files(folder_path)



def get_excel_files_to_sql(folder_path):
    excel_files = []
    for file_name in os.listdir(folder_path):
        print(file_name)
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            excel_files.append(file_name)
            parts = file_name.split(" - ")
            if len(parts) == 2:
                print(f"The file name is '{parts[0]}', from '{parts[1]}'.")
            else:
                print("Check file name. Not in format.")
    return excel_files