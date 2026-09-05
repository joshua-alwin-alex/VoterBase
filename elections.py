'''VoterBase is a sophisticated CLI Voting Portal
Copyright (C) 2026 Nandan B. Nair and Joshua Alwin Alex

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

with open("metadata.txt","r") as f1:
    username=(f1.readline()).strip("\n")
    password=(f1.readline()).strip("\n")

from main_program import con,cur
from permanent import *

def ex(x,values=None):
    cur.execute(x,values)

def initialise():
    try:
        ex('create database election')
    except:
        pass
    try:
        ex('use election')
    except:
        pass
    try:
        ex('create table voter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Voted varchar(10))')
    except:
        pass
    try:
        ex('create table candidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Votes int)')
    except:
        pass
    try:
        ex('create table possiblevoter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass
    try:
        ex('create table possiblecandidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Votes int)')
    except:
        pass

def voting():
    from tabulate import tabulate
    print("\n==============VOTING PORTAL==============")
    while True:
        ex("use election")
        ex("select Voted from voter")
        voted=cur.fetchall()
        ex("select * from voter")
        voters=cur.fetchall()
        flag=False
        for i in voted:
            if i[0]=="No":
                flag=True
                break
        else:
            print("All voters have voted.")
            print("Election completed successfully")
            return
        while flag:
            id=input("Enter VoterID:")
            pin=encode(input("Enter PIN:"))
            for j in voters:
                if j[0]==id:
                    if j[3]==pin:
                        if j[4]=="No":
                            ex("use election")
                            ex("select * from candidate")
                            candidates=cur.fetchall()
                            flag1=True
                            while flag1:
                                query="update voter set Voted = %s where VoterID = %s and PIN = %s"
                                data=("Yes", id, pin)
                                ex(query,data)
                                con.commit()
                                tablelist1=[]
                                for i in range(len(candidates)):
                                    j=candidates[i]
                                    table1={"Sl No.":i+1, "CandidateID":j[0], "Name":j[1], "DOB":j[2]}
                                    tablelist1.append(table1)
                                print(tabulate(tablelist1, headers="keys"))
                                n=input("Enter your choice of candidate (as number):")                                
                                if n.isdigit():
                                    if int(n)<=len(candidates):
                                        ex("select Votes from candidate") #Selecting originial vote count
                                        votevalue=cur.fetchall()
                                        votecount=votevalue[int(n)-1][0]
                                        ex("select CandidateID from candidate") #Selecting Candidate ID
                                        votecandidate=cur.fetchall()
                                        votecandidateid=votecandidate[int(n)-1][0]
                                        sql="update candidate set votes = %s where CandidateID = %s"
                                        val=(votecount+1, votecandidateid)
                                        ex(sql,val) #Updating vote count
                                        con.commit()
                                        flag1=False
                                    else:
                                        print("Please enter valid candidate number")
                                        query1="update voter set Voted = %s where VoterID = %s and PIN = %s"
                                        data1=("No", id, pin)
                                        ex(query1,data1)
                                        con.commit()
                                        flag1=True
                                        continue
                                else:
                                    print("Please enter the candidate's serial number")
                                    query1="update voter set Voted = %s where VoterID = %s and PIN = %s"
                                    data1=("No", id, pin)
                                    ex(query1,data1)
                                    con.commit()
                                    flag1=True
                                    continue
                            else:
                                flag=False
                                break
                        else:
                            print("You have already voted")
                            flag=False
                            break
                    else:
                        print("Please enter correct PIN")
                        flag=False
                        break
            else:
                print("Please enter valid VoterID")
                flag=False

            ch=input("Would you like to continue the election (y/n)?:")
            if ch in "Yy":
                continue
            else:
                password='password'
                ch1=input("Enter Admin password:")
                if ch1==password:
                    print("Election stopped by Admin")
                    return

def winnerdetails():
    print("\n==============ELECTION WINNER==============")
    ex("use election")
    ex("select * from candidate order by votes desc")
    candidates=cur.fetchall()
    j=candidates[0]
    ex("select sum(votes) from candidate")
    allvotes=cur.fetchall()
    s=allvotes[0][0]
    print("WINNER NAME:",j[1].upper())
    print("CANDIDATE ID:",j[0])
    print("DATE OF BIRTH:",j[2])
    print("VOTES RECEIVED:",j[4])
    print("VOTE SHARE:",(j[4]/s)*100)

def resultstable():
    from tabulate import tabulate
    print("\n==============ELECTION RESULT==============")
    ex("use election")
    ex("select * from candidate order by votes desc")
    candidates=cur.fetchall()
    tablelist1=[]
    for i in range(len(candidates)):
        j=candidates[i]
        table1={"Sl No.":i+1, "CandidateID":j[0], "Name":j[1], "DOB":j[2], "Votes Reveived":j[4]}
        tablelist1.append(table1)
    print(tabulate(tablelist1, headers="keys"))

def saveresult():
    ex("use election")
    ex("select * from candidate order by votes desc")
    candidates=cur.fetchall()
    data=[]
    for i in candidates:
        data.append([i[0],i[1],i[2],i[4]])
    import csv
    ch=input("Enter the name of the csv file to save the result into:")
    with open(ch+".csv","w",newline='') as f1:
        w1=csv.writer(f1)
        w1.writerow(["CandidateID","Name","DOB","Votes Received"])
        w1.writerows(data)
    print("Election Result saved to",ch+".csv")

def resultsbarchart():
    import matplotlib
    import tkinter
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    import numpy as np
    ch=input("Enter the name of the png file to save the bar chart into:")
    ex("use election")
    ex("select * from candidate order by votes desc")
    candidates=cur.fetchall()
    name=[];votes=[]
    for i in candidates:
        name.append(i[1])
        votes.append(i[4])
    votes1=np.array(votes)
    plt.bar(name,votes1)
    plt.title("Election Results")
    plt.xlabel("Candidate Name")
    plt.ylabel("Votes Received") 
    plt.savefig(ch+".png",dpi=300)
    plt.close()
    from PIL import Image
    img=Image.open(ch+".png")
    print("Bar Chart successfully saved to PNG file")
    img.show()
    input("Press Enter to go back to Election Portal")

def resultspiechart():
    import matplotlib
    import tkinter
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    import numpy as np
    ch=input("Enter the name of the png file to save the pie chart into:")
    ex("use election")
    ex("select * from candidate order by votes desc")
    candidates=cur.fetchall()
    name=[];votes=[]
    for i in candidates:
        name.append(i[1])
        votes.append(i[4])
    votes1=np.array(votes)
    plt.pie(votes1, labels=name,
            labeldistance=1.1,
            autopct="%1.1f%%",
            pctdistance=0.6)
    plt.title("Election Results")
    plt.savefig(ch+".png",dpi=300)
    plt.close()
    from PIL import Image
    img=Image.open(ch+".png")
    print("Pie Chart successfully saved to PNG file")
    img.show()
    input("Press Enter to go back to Election Portal")

def electionportal():
    while True:
        print("\n==============ELECTION PORTAL==============")
        n=input('\n1. Start Election' \
        '\n2. Display Winner Details' \
        '\n3. Display Results in Table Format' \
        '\n4. Save Result to CSV File' \
        '\n5. Display Results in Bar Chart Format' \
        '\n6. Display Results in Pie Chart Format' \
        '\n7. Go Back to Configuration Portal' \
        '\nEnter the choice of action:')
        if n=='1':
            voting()
        elif n=='2':
            winnerdetails()
        elif n=='3':
            resultstable()    
        elif n=='4':
            saveresult()
        elif n=='5':
            resultsbarchart()
        elif n=='6':
            resultspiechart()
        elif n=='7':
            break
        else:
            print("Please enter valid choice of action")      