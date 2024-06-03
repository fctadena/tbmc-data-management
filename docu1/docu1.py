import os




#CHECK IF FILE "Envelope Recipient Report.csv" EXIST
def file_checker():
    #File "Envelope Recipient Report.csv" extracted from Docusign
    if os.path.exists("Envelope Recipient Report.csv"):
        print("ok")
    else:
        print("nope")
file_checker()




    



    