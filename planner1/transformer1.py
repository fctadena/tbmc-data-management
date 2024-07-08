import pandas as pd



def transformer1(file_path):
    data = pd.read_excel(file_path)
    return data



def getting_idxs(data):
    indexes = []
    for idx, i in enumerate(data['Assigned To']):
        assigned_list = str(i).split(';')
        if len(assigned_list) > 1:
            indexes.append(idx)
    return indexes







def populate_new_data(data, idxs):
    new_data = data.drop(data.index)
    for idxn, assigned_to in enumerate(data['Assigned To']): #for the 'Assigned To' column, find the row where the index is in idxs.
        if idxn in idxs:
            assigned_list = str(assigned_to).split(';')
            new_rows = [[]]
            for assignee in assigned_list: #do the insertion of the task on the 'new_data' dataframe
                task_id = data.loc[idxn, 'Task ID']
                task_name = data.loc[idxn, 'Task Name']
                bucket_name = data.loc[idxn, 'Bucket Name']
                progress = data.loc[idxn, 'Progress']
                priority = data.loc[idxn, 'Priority']
                assigned_to = assignee #The changes
                created_by = data.loc[idxn, 'Created By']
                created_date = data.loc[idxn, 'Created Date']
                start_date = data.loc[idxn, 'Start date']
                due_date = data.loc[idxn, 'Due date']
                is_recurring = data.loc[idxn, 'Is Recurring']
                late = data.loc[idxn, 'Late']
                completed_date = data.loc[idxn, 'Completed Date']
                completed_by = data.loc[idxn, 'Completed By']
                com_checklist_items = data.loc[idxn, 'Completed Checklist Items']
                checklist_items = data.loc[idxn, 'Checklist Items']
                labels = data.loc[idxn, 'Labels']
                description = data.loc[idxn, 'Description']

                
                new_row = [
                    task_id,
                    task_name,
                    bucket_name,
                    progress,
                    priority,
                    assigned_to,
                    created_by,
                    created_date,
                    start_date,
                    due_date,
                    is_recurring,
                    late, 
                    completed_date,
                    completed_by,
                    com_checklist_items,
                    checklist_items, 
                    labels, 
                    description
                ]
                
                new_data.loc[len(new_data)] = new_row
       
    return new_data


def concatenate_data(data, new_data):
    concatenated_data = pd.concat([data, new_data], ignore_index=True)
    return concatenated_data


def delete_rows(concatenated_data, idxs):
    final_data = concatenated_data.drop(idxs)
    return final_data





def main(file_path, output_path):
    data = transformer1(file_path)
    idxs = getting_idxs(data)
    new_data = populate_new_data(data, idxs)
    concatenated_data = concatenate_data(data, new_data)
    final_data = delete_rows(concatenated_data, idxs)
    final_data.to_excel(output_path, index=False)
    return final_data



# file_path = 'Project Timeline Update.xlsx'
# file_path = r"C:\Users\Francis\00_ML\00_Power BI\docu1\tbmc-data-management\data\project_timeline\Project Timeline Update.xlsx"
file_path = r"C:\Users\PHTadenaFr\Documents\tbmc-data-management\data\project_timeline\Project Timeline Update.xlsx"

output_path = 'Transformed_Project_Timeline_Update.xlsx'
# output_path = r'C:\Users\PHTadenaFr\Documents\tbmc-data-management\data\project_timeline\Project Timeline Update.xlsx'
# output_path = r'data\project_timeline\Project Timeline Update.xlsx'


transformed_data = main(file_path, output_path)
print(transformed_data)
