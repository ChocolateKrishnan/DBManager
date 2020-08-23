import pyodbc
import getpass
import datetime
from prettytable import PrettyTable
def columngetter(tablename):
    detailcursor=connection.cursor()
    detailcursor.execute("select column_name from information_schema.columns WHERE TABLE_NAME = N'"+tablename+"'")
    tablecolumns=[]
    for i in detailcursor:
        a=str(i)
        tablecolumns.append(a[2:-4])
    detailcursor.close()
    return tablecolumns
def tablegetter():
    detailcursor=connection.cursor()
    detailcursor.execute("SHOW TABLES")
    tablestable=[]
    for i in detailcursor:
        a=str(i)
        b=a[2:-4]
        tablestable.append(b)
    detailcursor.close()
    return tablestable
def tablechecker():
    print ("Would you like me to get the list of tables? (Y/N)")
    response=str(input())[0]
    tables=tablegetter()
    if response=="Y":
        j=1
        for i in tables:
           print (str(j)+". "+i)
           j=j+1
    print ("Enter the table name to continue")
    tablename=str(input())
    if tablename in tables:
        return tablename
    else:
        print ("Invalid Table!")
        tablechecker()
def select(tablename):
    detailcursor=connection.cursor()
    mycursor=connection.cursor()
    print ("1.Would you like to construct the query? (I can construct very simple query) \n2. Do you have the query?")
    queryoption=int(input())
    if queryoption==1:
        query="SELECT "
        print ("Plese enter the column(s) that you would like to view (please provide ',' between column names if there are more than one columns)")
        print ("To choose all columns you can enter * ")
        columns=str(input())
        if columns.endswith(",") or columns.endswith(" "):
            columns=columns[:-1]
        query=query+columns+" FROM "+tablename
        print ("Do you have any filter condition? (Y/N)")
        question1=str(input())
        if question1=="Y":
            print ("Based on how many column do I have to filter")
            question2=int(input())
            query=query+" WHERE "
            for i in range(0,question2):
                print ("Enter the column "+str(i+1))
                filtercolumn=str(input())
                print("What is creteria?")
                creteria=str(input())
                query=query+filtercolumn+creteria
                if (i+1)>=1 and (i+1)<question2:
                    print("AND or OR")
                    question3=str(input())
                    query=query+" "+question3+" "
        print (query)
    if queryoption==2:
        query=str(input())
    tablecolumns=columngetter(tablename)
    displaytable=PrettyTable()
    displaytable.field_names=tablecolumns
    mycursor.execute(query)
    for i in mycursor:
        a=[]
        for j in i:
            a.append(j)
        displaytable.add_row(a)
    print(displaytable)
    detailcursor.close()
    mycursor.close()
def insert(tablename):
    mycursor=connection.cursor()
    print ("1.Would you like to construct the query? (I can construct very simple query) \n2. Do you have the query?")
    queryoption=int(input())
    if queryoption==1:
        print ("Would you like me to get the columns of the table? (Y/N)")
        columns=columngetter(tablename)
        columns=tuple(columns)
        if str(input())[0]=='Y':
            print(columns)
        query="INSERT INTO "+tablename+" ("
        for i in columns:
            query=query+i+","
        query=query[:-1]+") VALUES ("
        for i in columns:
            print ("Enter the value for "+i)
            query=query+str(input())+","
        query=query[:-1]+");"
        print (query)
        mycursor.execute(query) 
        print ("Query executed")
    if queryoption==2:
        query=str(input())
    connection.commit()
    mycursor.close()
def update(tablename):
    mycursor=connection.cursor()
    print ("1.Would you like to construct the query? (I can construct very simple query) \n2. Do you have the query?")
    queryoption=int(input())
    if queryoption==1:
        print ("Would you like me to get the columns of the table? (Y/N)")
        columns=columngetter(tablename)
        columns=tuple(columns)
        if str(input())[0]=='Y':
            print(columns)
        query="UPDATE "+tablename+" SET "
        print ("How many columns do you want to update for the records?")
        number=int(input())
        for i in range (0,number):
            print("Enter the column name and its change value. \nExample Column_name='value'")
            query=query+str(input())+","
        query=query[:-1]
        print ("Do you have any filter condition? (Y/N)")
        question1=str(input())
        if question1=="Y":
            print ("Based on how many column do I have to filter")
            question2=int(input())
            query=query+" WHERE "
            for i in range(0,question2):
                print ("Enter the column "+str(i+1))
                filtercolumn=str(input())
                print("What is creteria?")
                creteria=str(input())
                query=query+filtercolumn+creteria
                if (i+1)>=1 and (i+1)<question2:
                    print("AND or OR")
                    question3=str(input())
                    query=query+" "+question3+" "
    if queryoption==2:
        query=str(input())
    connection.commit()
    mycursor.close()
def delete(tablename):
    mycursor=connection.cursor()
    print ("1.Would you like to construct the query? (I can construct very simple query) \n2. Do you have the query?")
    queryoption=int(input())
    if queryoption==1:
        print ("Would you like me to get the columns of the table? (Y/N)")
        query="DELETE FROM"+tablename
        print ("Do you have any filter condition? (Y/N)")
        question1=str(input())
        if question1=="Y":
            print ("Based on how many column do I have to filter")
            question2=int(input())
            query=query+" WHERE "
            for i in range(0,question2):
                print ("Enter the column "+str(i+1))
                filtercolumn=str(input())
                print("What is creteria?")
                creteria=str(input())
                query=query+filtercolumn+creteria
                if (i+1)>=1 and (i+1)<question2:
                    print("AND or OR")
                    question3=str(input())
                    query=query+" "+question3+" "
    if queryoption==2:
        query=str(input())
    connection.commit()
    mycursor.close()
def passquery():
    mycursor=connection.cursor()
    query=str(input())
    mycursor.execute(query)
    connection.commit()
    mycursor.close()
def main():
    print ("Please select operation you want to perform")
    print ("1. View Records")
    print ("2. Add Records")
    print ("3. Modify or Change Records")
    print ("4. Delete Records")
    print ("5. Execute Queries")
    print ("6. Exit")
    option=int(input())
    if option==1:
        tablename=tablechecker()
        select(tablename)
        main()
    elif option==2:
        tablename=tablechecker()
        insert(tablename)
        main()
    elif option==3:
        tablename=tablechecker()
        update(tablename)
        main()
    elif option==4:
        tablename=tablechecker()
        delete(tablename)
        main()
    elif option==5:
        print ("You are not restricted to any particular table. Hence you can perform joins and can view the data")
        passquery()
        main()
    elif option==6:
        exit
    else:
        print ("Invalid option! Try Again")
        main()
print ("Welcome! Select the correct ODBC driver to begin")
driverlist=pyodbc.drivers()
j=1
for i in driverlist:
    print (str(j)+"."+i)
    j=j+1
driverselect=int(input())
driver=driverlist[driverselect-1]
print ("Please enter the server name")
server=str(input())
print ("Please enter the database name")
database=str(input())
print ("Please enter the user name")
user=str(input())
password=getpass.getpass()
connection=pyodbc.connect("DRIVER={"+driver+"}; SERVER="+server+";DATABASE="+database+"; UID="+user+"; PASSWORD="+password+";")     
main()