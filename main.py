import csv
import pandas as pd

fileAddress = "library.csv"
fpPandas = pd.read_csv(fileAddress)

def addRecord () :
    StudentID = input("\nEnter Student ID")
    StudentName = input("Enter Student Name: ")
    BookName = input("Enter Book Name: ")
    IssueDate = input("Enter Issue Date: ")
    ReturnDate = input("Enter Return Date: ")
    RegistrationDetails = input("Enter Registration Details: ")
    BookAvailability = input("Enter Book Availability: ")

    newRecord = [
        StudentID,
        StudentName.lower(),
        BookName,
        IssueDate,
        ReturnDate,
        RegistrationDetails,
        BookAvailability
    ]

    fp = open("library.csv", 'a', newline = '')

    writer = csv.writer(fp)
    writer.writerow(newRecord)
    print("\nRECORD ADDED")

    fp.close()
    input()

def readRecord () :
    fpPandas = pd.read_csv(fileAddress)

    readChoice = input("\nSearch Options: \n1. View Table\n2. View by Student ID\n3. View by Student Name\nEnter: ")
    
    match int(readChoice):
        case 1:
            print(fpPandas)
        case 2:
            searchID = input("Enter the student ID to be searched: ")
            searchID = int(searchID)
            IDLi = list(fpPandas["Student ID"])
            for i in range(len(IDLi)):
                if IDLi[i] == searchID:
                    print(fpPandas.iloc[i])
                    print()
                    return
            print("\nID ENTERED IS NOT IN THE FILE")
        case 3:
            searchName = input("Enter the name of the student to be searched: ")
            searchName = searchName.lower()
            nameLi = list(fpPandas["Student Name"])
            for i in range(len(nameLi)):
                if nameLi[i] == searchName:
                    print(fpPandas.iloc[i])
                    print()
                    return
            print("\nNAME ENTERED IS NOT IN THE FILE")
        case _:
            print("\nINVALID INPUT")

    input()

def speciUpdate (searchVar, pandasList) :
    fpPandas = pd.read_csv(fileAddress)

    for i in range(len(pandasList)):
        if pandasList[i] == searchVar:
            print("\nSelect Editing option")
            colLi = list(fpPandas.columns)
            for j in range(2, len(colLi)):
                print(f"{j-1}. {colLi[j]}")
            choice = input("Enter: ")

            match int(choice):
                case 1:
                    BookName = input("Enter Book Name: ")
                    fpPandas.loc[i, "Book Name"] = BookName
                    fpPandas.to_csv(fileAddress, index=False)
                case 2:
                    IssueDate = input("Enter Issue Date: ")
                    fpPandas.loc[i, "Issue Date"] = IssueDate
                    fpPandas.to_csv(fileAddress, index=False)
                case 3:
                    ReturnDate = input("Enter Return Date: ")
                    fpPandas.loc[i, "Return Date"] = ReturnDate
                    fpPandas.to_csv(fileAddress, index=False)
                case 4:
                    RegistrationDetails = input("Enter Registration Details: ")
                    fpPandas.loc[i, "Registration Details"] = RegistrationDetails
                    fpPandas.to_csv(fileAddress, index=False)
                case 5:
                    BookAvailability = input("Enter Book Availability: ")
                    fpPandas.loc[i, "Book Availability"] = BookAvailability
                    fpPandas.to_csv(fileAddress, index=False)
                case _:
                    print("\nINVALID INPUT")
                    return
            
            print("\nDATA UPDATED")


def updateRecord () :
    fpPandas = pd.read_csv(fileAddress)

    choice = input("\nSearch Options(for Editing): \n1. Search by Student ID\n2. Search by Student Name")
    
    match int(choice):
        case 1:
            searchID = input("Enter the Student ID to be searched: ")
            searchID = int(searchID)
            if (searchID not in set(fpPandas["Student ID"])): 
                print("\nID NOT IN DATA")
                return
            IDLi = list(fpPandas["Student ID"])
            speciUpdate(searchID, IDLi)
        case 2:
            searchName = input("Enter the name of the student to be searched: ")
            searchName = searchName.lower()
            if (searchName not in set(fpPandas["Student Name"])): 
                print("\nNAME NOT IN DATA")
                return
            nameLi = list(fpPandas["Student Name"])
            speciUpdate(searchName, nameLi)
        case _:
            print("\nINVALID INPUT")    
    input()        

def popRecord () :
    fpPandas = pd.read_csv(fileAddress)

    choice = input("\nSearch Options(for Deleting): \n1. Search by Student ID\n2. Search by Student Name")
    
    match int(choice):
        case 1:
            searchID = input("Enter the Student ID to be searched: ")
            searchID = int(searchID)
            if (searchID not in set(fpPandas["Student ID"])): 
                print("\nID NOT IN DATA")
                return
            fpPandas = fpPandas[fpPandas["Student ID"] != searchID]
            fpPandas.to_csv(fileAddress, index=False)
        case 2:
            searchName = input("Enter the name of the student to be searched: ")
            searchName = searchName.lower()
            if (searchName not in set(fpPandas["Student Name"])): 
                print("\nNAME NOT IN DATA")
                return
            fpPandas = fpPandas[fpPandas["Student Name"] != searchName]
            fpPandas.to_csv(fileAddress, index=False)
        case _:
            print("\nINVALID INPUT")
    input()

flag = True
while (flag) :
    choice = input("\n\n# Library Management System\n1. Add record\n2. Read record\n3. Update record\n4. Delete record\n5. Exit\nEnter: ")

    if not choice.isdigit():
        print("INVALID INPUT")
        continue

    match int(choice):
        case 1:
            addRecord()
        case 2:
            readRecord()
        case 3:
            updateRecord()
        case 4:
            popRecord()
        case 5:
            flag = False

        case _:
            print("INVALID INPUT")
            input()