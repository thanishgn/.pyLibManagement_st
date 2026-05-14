import pandas as pd
import streamlit as st
import csv

DTYPES = {
    "Student ID": int,
    "Student Name": str,
    "Book Name": str,
    "Issue Date": str,
    "Return Date": str,
    "Registration Details": str,
    "Book Availability": str
}

fileAddress = "library.csv"
fpPandas = pd.read_csv(fileAddress, dtype = DTYPES)

searchView = fpPandas

st.title("Library Management System")
# st.header("Table")
# st.table(fpPandas)

userChoice = st.radio("", [
    "Add Record",
    "Search Records",
    "Update Record",
    "Pop Record"
], horizontal = True)

if (userChoice == "Add Record") :
    with st.form("add_form", clear_on_submit=True):
        StudentID = st.text_input("Student ID")
        StudentName = st.text_input("Student Name")
        BookName = st.text_input("Book Name")
        IssueDate = st.text_input("Issue Date")
        ReturnDate = st.text_input("Return Date")
        RegistrationDetails = st.text_input("Registration Details")
        BookAvailability = st.selectbox("Book Availability", ["Yes", "No"])

        submitted = st.form_submit_button("Add Record")
        if (submitted):
            if ((not StudentID) or (not StudentName)):
                st.error("Student ID and Student Name are required.")
            else:
                newRecord = [
                    StudentID,
                    StudentName.lower(),
                    BookName,
                    IssueDate,
                    ReturnDate,
                    RegistrationDetails,
                    BookAvailability
                ]

                fp = open(fileAddress, 'a', newline='')
                writer = csv.writer(fp)
                writer.writerow(newRecord)
                fp.close()

                st.success("RECORD ADDED")

elif (userChoice == "Search Records"):

    fpPandas = pd.read_csv(fileAddress, dtype = DTYPES)

    readChoice = st.radio("Search Options", ["View Table", "View by Student ID", "View by Student Name"])

    if readChoice == "View Table":
        st.dataframe(fpPandas)

    elif readChoice == "View by Student ID":
        searchID = st.text_input("Enter the student ID to be searched")
        if st.button("Search"):
            try:
                searchID = int(searchID)
                IDLi = list(fpPandas["Student ID"])
                found = False
                for i in range(len(IDLi)):
                    if IDLi[i] == searchID:
                        st.dataframe(fpPandas.iloc[[i]])
                        found = True
                        break
                if not found:
                    st.error("ID ENTERED IS NOT IN THE FILE")
            except ValueError:
                st.error("Please enter a valid numeric Student ID.")

    elif readChoice == "View by Student Name":
        searchName = st.text_input("Enter the name of the student to be searched")
        if st.button("Search"):
            
            searchName = searchName.lower()
            nameLi = list(fpPandas["Student Name"])
            found = False
            for i in range(len(nameLi)):
                if nameLi[i] == searchName:
                    st.dataframe(fpPandas.iloc[[i]])
                    found = True
                    break
            if not found:
                st.error("NAME ENTERED IS NOT IN THE FILE")

elif (userChoice == "Update Record"):

    fpPandas = pd.read_csv(fileAddress, dtype = DTYPES)

    choice = st.radio("Search Options (for Editing)", ["Search by Student ID", "Search by Student Name"])

    def speciUpdate(searchVar, searchCol):
        fpPandas = pd.read_csv(fileAddress, dtype = DTYPES)
        pandasList = list(fpPandas[searchCol])
        colLi = list(fpPandas.columns)
        ediColLi = colLi[2:]

        for i in range(len(pandasList)):
            if pandasList[i] == searchVar:
                st.write("Record found:")
                st.dataframe(fpPandas.iloc[[i]])

                editCol = st.selectbox("Select field to edit", ediColLi)

                if (editCol == "Book Availability"):
                    new_value = st.selectbox("New value", ["Yes", "No"])
                else:
                    new_value = str(st.text_input(f"New value for {editCol}"))
                    

                if (st.button("Save Changes")):
                    fpPandas.loc[i, editCol] = new_value
                    fpPandas.to_csv(fileAddress, index = False)
                    st.success("DATA UPDATED")
                return

        st.error("Record not found.")

    if (choice == "Search by Student ID"):
        searchID = st.text_input("Enter the Student ID to be searched")
        if (st.button("Find")):
            try:
                searchID = int(searchID)
                if (searchID not in set(fpPandas["Student ID"])):
                    st.error("ID NOT IN DATA")
                else:
                    st.session_state["update_id"] = searchID
                    st.session_state["update_mode"] = "id"
            except ValueError:
                st.error("Please enter a valid numeric Student ID.")

        if (st.session_state.get("update_mode") == "id"):
            speciUpdate(st.session_state["update_id"], "Student ID")


    elif (choice == "Search by Student Name"):
        searchName = st.text_input("Enter the name of the student to be searched")
        if (st.button("Find")):
            searchName = searchName.lower()
            if (searchName not in set(fpPandas["Student Name"])):
                st.error("NAME NOT IN DATA")
            else:
                st.session_state["update_name"] = searchName
                st.session_state["update_mode"] = "name"

        if (st.session_state.get("update_mode") == "name"):
            speciUpdate(st.session_state["update_name"], "Student Name")

elif (userChoice == "Pop Record") :
    fpPandas = pd.read_csv(fileAddress, dtype = DTYPES)

    choice = st.radio("Search Options (for Deleting)", ["Search by Student ID", "Search by Student Name"])

    if (choice == "Search by Student ID"):
        searchID = st.text_input("Enter the Student ID to be searched")
        if (st.button("Find")):
            try:
                searchID = int(searchID)
                if (searchID not in set(fpPandas["Student ID"])):
                    st.error("ID NOT IN DATA")
                else:
                    st.dataframe(fpPandas[fpPandas["Student ID"] == searchID])
                    st.session_state["delete_id"] = searchID
                    st.session_state["delete_mode"] = "id"
            except ValueError:
                st.error("Please enter a valid numeric Student ID.")

        if (st.session_state.get("delete_mode") == "id"):
            if (st.button("Confirm Delete")):
                fpPandas = fpPandas[fpPandas["Student ID"] != st.session_state["delete_id"]]
                fpPandas.to_csv(fileAddress, index=False)
                del st.session_state["delete_mode"]
                st.success("RECORD DELETED")
                st.rerun()

    elif (choice == "Search by Student Name"):
        searchName = st.text_input("Enter the name of the student to be searched")
        if (st.button("Find")):
            searchName = searchName.lower()
            if (searchName not in set(fpPandas["Student Name"])):
                st.error("NAME NOT IN DATA")
            else:
                st.dataframe(fpPandas[fpPandas["Student Name"] == searchName])
                st.session_state["delete_name"] = searchName
                st.session_state["delete_mode"] = "name"

        if (st.session_state.get("delete_mode") == "name"):
            if (st.button("Confirm Delete")):
                fpPandas = fpPandas[fpPandas["Student Name"] != st.session_state["delete_name"]]
                fpPandas.to_csv(fileAddress, index = False)
                del st.session_state["delete_mode"]
                st.success("RECORD DELETED")
                st.rerun()
