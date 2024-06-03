import os



#docu1.py
#PURPOSE: To save csv generated data from docusign to aws database.



#CHECK IF FILE "Envelope Recipient Report.csv" EXIST
def file_checker():
    #File "Envelope Recipient Report.csv" extracted from Docusign
    print("Checking if 'Envelope Recipient Report.csv' exist")
    if os.path.exists("Envelope Recipient Report.csv"):
        print("'Envelope Recipient Report.csv' exist.")
        print("Proceeding to update database.")

        #add function here..


    else:
        print("'Envelope Recipient Report.csv' does not exist.")



file_checker()




    



    