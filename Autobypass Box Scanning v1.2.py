#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#My program function library, import all libraries
import numpy as np
import pandas as pd
import tkinter as tk
import os
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime


# In[ ]:


#Get the current directory for easy debugging
cwd = os.getcwd()
print(cwd)


# In[ ]:


#Data base connection for SQL Server (PLUGIN)
# -*- coding: utf-8 -*-
"""
Spyder Editor
SQL read query
"""

#Import SQL libraries
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import urllib


#Setting all credential and parameters. 
server = 'Redacted\Redacted'
database1 = 'CLASS'
database2 = 'reference'

#query1 = "SELECT ID FROM dbo.Redacted"
#query2 = "SELECT equip_id FROM dbo.Redacted"
query3 = "SELECT MA_ID, container_ID FROM mam_asm.Redacted"

#Display information
username = 'Redacted'
password = 'Redacted'
print("=====================================================")
print("     Product Parent and ID matching scanning")
print("=====================================================")
print("version 1.2")
print("1/24/2022")
print("Author: Zac Tey")
print("Database has 5-15 minutes delay")
print("Log files stored as Log.txt in the same directory")
print("------------------------------------------")

#Function to establish conn and process query + conn, returns a dataframe as a result
def read_sql(query, db_name):
    conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}', host=server, database=db_name, 
                      user=username, password=password)
    df = pd.read_sql(query, conn)
    return df


# In[ ]:


#df1 = read_sql(query1, database1)
#df1 = pd.DataFrame(df1)

#df2 = read_sql(query2, database2)
#df2 = pd.DataFrame(df2)

#=========TESTING...IN PRODUCTION===========
#df3 = read_sql(query3, database2)
#df3 = pd.DataFrame(df3)
#df3.columns=['PARENT LOT','CARRIER']
#df3.tail(10)


# In[ ]:


#function to check where the LOT ID exist in the database
def matchID (df,scanp, scanc):
    df['PARENT LOT']=df['PARENT LOT'].str.strip()
    df['CARRIER']=df['CARRIER'].str.strip()
    
    #Called 2 copies of dataframes from the input df
    df1 = df.copy()
    df2 = df.copy()
    
    # This will result in an empty dataframe in dfrow if no matching values are found. 
    dfrow = df1.loc[df1['PARENT LOT'] == scanp]
    if len(dfrow) == 0:
        #Display message if it is empty dataframe
        print("NO PARENT LOT ID FOUND FOR:" + scanp)
        messagebox.showerror("NO ID FOUND","NO PARENT LOT ID FOUND, Please click OK to continue")
        #Setting variable to trace the event. 
        chkp = "not valid"
        #Printing the result by creating/updating text file as log file
        with open('log.txt', "a") as text_file:
            print("CHECK PARENT:" +chkp , file=text_file)
    else: 
        #Setting variable to trace the event. 
        chkp = "valid"
        #Printing the result by creating/updating text file as log file
        print("CHECK PARENT: " + chkp)
        with open('log.txt', "a") as text_file:
            print("CHECK PARENT:" +chkp , file=text_file)   
        
        
    # This will result in an empty dataframe in dfrowc if no matching values are found. 
    dfrowc = df2.loc[df2['CARRIER'] == scanc]
    if len(dfrowc) == 0:
        #Display message if it is empty dataframe
        print("NO CARRIER ID FOUND FOR:" + scanc)
        print("")
        messagebox.showerror("NO ID FOUND","NO CARRIER ID FOUND, Please click OK to continue")
        #Setting variable to trace the event.
        chkc = "not valid"
        #Printing the result by creating/updating text file as log file
        with open('log.txt', "a") as text_file:
            print("CHECK CARRIER:" +chkc, file=text_file)
        #Display the correct matching for the CARRIER. if the PARENT is not empty
        if len(dfrow) != 0:
            print(dfrow)  
    else: 
        #Setting variable to trace the event.
        chkc = "valid"
        #Display message if it is empty dataframe
        print("CHECK CARRIER:" +chkc)
        print("")
        #Printing the result by creating/updating text file as log file
        with open('log.txt', "a") as text_file:
            print("CHECK CARRIER:" +chkc, file=text_file)
        #Display the correct matching for the PARENT. if the CARRIER is not empty
        if len(dfrow) == 0:
            print(dfrowc)
    
    return chkp,chkc


# In[ ]:


#Function to compare parent lot with carrier ID, input takes in a 
#df, 2 event checking variables and 2 scanned input CARRIER and PARENT
def compare(df, chkp,chkc,scanp,scanc):

    #First filter the Row using PARENT ID
    dfrow = df.loc[df['PARENT LOT'] == scanp]
    #Condition: If both PARENT and CARRIER markers showing valid, check the filtered row's CARRIER ID with the scanned
    #carrier ID. 
    if (chkp == "valid") and (chkc == "valid") and (dfrow['CARRIER'].values[0] == scanc):  
        #Print "MATCH" if conditions are met.
        print(">>>>MATCH<<<<")
        #Printing the result by creating/updating the text file as log file. 
        with open('log.txt', "a") as text_file:
            print("MATCH", file=text_file)
        #Show the message box if the result is a MATCH. 
        messagebox.showinfo("ID MATCH","MATCH, Please click OK to continue")       
        
    #Check the marker variable for PARENT and CARRIER, whether if they are valid IDs or not.    
    elif (chkp == "valid") and (chkc == "valid"):
        #print the result NOT MATCH 
        print("NOT MATCH")
        #print the result by creating or updating a text file.
        with open('log.txt', "a") as text_file:
            print(">>>>NOT MATCH<<<<", file=text_file)
        #Show message box for ID not match for both PARENT and CARRIER.
        messagebox.showwarning("ID NOT MATCH","NOT MATCH, Please click OK to continue")
        


# In[ ]:


#function to scan parent lot from the magazine traveller.
def alert_scanp():
    #Remove the ROOT window.
    ROOT = tk.Tk()
    ROOT.withdraw()
    #Simple Dialog Box pop out to prompt for user to input or scan the PARENT ID from the traveller. 
    scanp = simpledialog.askstring(title="SCAN PARENT LOT",
                                      prompt="Please scan PARENT LOT from traveller:")
    #Print out the parent ID that is being successfully scanned. 
    print("PARENT LOT:   "+ scanp)
    #Record this scanned PARENT ID by creating or updating the text file in the same directory. 
    with open('log.txt', "a") as text_file:
        print("------------------------------------------", file=text_file)
        print("PARENT LOT: "+ scanp, file=text_file)
    #Return the scanned value.
    return scanp


# In[ ]:


#function to scan carrier ID from magazine. 
def alert_scanc():
    #Remove the ROOT window.
    ROOT = tk.Tk()
    ROOT.withdraw()
    #Simple dialog box pip out to prompt for user to input or scan the PARENT ID from the magazine 2D Barcode.
    scanc = simpledialog.askstring(title="SCAN MAGAZINE",
                                      prompt="Please scan CARRIER ID:   ")
    
    print("CARRIER ID:   "+ scanc)
    with open('log.txt', "a") as text_file:
        print("CARRIER ID:   "+ scanc, file=text_file)
    return scanc


# In[ ]:


#Main Program to reloop
while True:
    #main program
    print()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    df = read_sql(query3, database2)
    data = pd.DataFrame(df)
    
    data.columns=['PARENT LOT','CARRIER']
    scanp = alert_scanp()
    scanc = alert_scanc()
    print("")
    chkp,chkc = matchID (data, scanp, scanc)
    compare(data, chkp,chkc,scanp,scanc)
    print(dt_string)
    
    with open('log.txt', "a") as text_file:
        print(""+dt_string, file=text_file)
    print("------------------------------------------")
    continue


# In[ ]:





# In[ ]:




