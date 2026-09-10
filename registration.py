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

def permanentvoterregistration():
    voter()

def permanentcandidateregistration():
    candidate()

def ex(x,values=None):
    cur.execute(x,values)

def initialise():
    try:
        ex('create database votebase')
    except:
        pass
    try:
        ex('use votebase')
    except:
        pass
    try:
        ex('create table voter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass
    try:
        ex('create table candidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass
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
        ex('create table possiblecandidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass

def voterregister():
    print("\n==============VOTER REGISTRATION PORTAL==============")
    while True:
        n=input(("\n1. Register as permanent voter" \
        "\n2. Register for election" \
        "\n3. Go Back to Configuration Portal" \
        "\nEnter the choice of action:"))
        if n=='1':
            permanentvoterregistration()
        elif n=='2':
            id=input("Enter VoterID:")
            pin=encode(input("Enter PIN:"))
            ex("use votebase")
            ex("select * from voter")
            voters=cur.fetchall()
            for i in voters:
                if i[0]==id:
                    if i[3]==pin:
                        try:
                            ex("use election")
                            data=(i[0], i[1], i[2], i[3])
                            query='insert into possiblevoter values (%s, %s, %s, %s)'
                            ex(query, data)
                            con.commit()
                            print("Voter application accepted")
                            input("\nPress Enter to go back to Voter Registration Portal")
                            break
                        except:
                            print("Duplicate entry is not allowed")
                            input("\nPress Enter to go back to Voter Registration Portal")
                            break
                    else:
                        print("Please enter correct PIN")
                        break
            else:
                print("Your Voter application was rejected.")
                print("Please register as a permanent voter first.")
        elif n=='3':
            break
        else:
            print("Please enter valid choice of action")

def votereligibility():
    from tabulate import tabulate
    ex('select * from possiblevoter')
    t=cur.fetchall()
    if len(t)!=0:
        while True:
            n=input(("\n1. Select voters for this election" \
            "\n2. Go Back to Admin Portal" \
            "\nEnter the choice of action:"))
            if n=='1':
                ex("use election")
                ex("delete from voter")
                print("\n==============VOTER SELECTION PORTAL==============")
                ex("use election")
                ex("select * from possiblevoter")
                voters=cur.fetchall()
                for i in range(len(voters)):
                    j=voters[i]
                    table=[{"Sl No.":i+1, "VoterID":j[0], "Name":j[1], "DOB":j[2]}]
                    print("\n"+tabulate(table, headers="keys"))
                    n=input("Would you like to select this voter (y/n)?:")
                    if n in "Yy":
                        ex("use election")
                        data=(j[0], j[1], j[2], j[3], "No")
                        query='insert into voter values (%s, %s, %s, %s, %s)'
                        ex(query, data)
                        con.commit()
                        print("Voter added to electoral rolls")
            elif n=='2':
                break
            else:
                print("Please enter valid choice of action")
    else:
        print("No voters have registered for this election")
        print("Please ask voters to register for this election before selecting voters")

def candidateregister():
    print("\n==============CANDIDATE REGISTRATION PORTAL==============")
    while True:
            n=input(("\n1. Register as permanent candidate" \
            "\n2. Register for election" \
            "\n3. Go Back to Configuration Portal" \
            "\nEnter the choice of action:"))
            if n=='1':
                permanentcandidateregistration()
            elif n=='2':
                id=input("Enter CandidateID:")
                pin=encode(input("Enter PIN:"))
                ex("use votebase")
                ex("select * from candidate")
                candidate=cur.fetchall()
                for i in candidate:
                    if i[0]==id:
                        if i[3]==pin:
                            try:
                                ex("use election")
                                data=(i[0], i[1], i[2], i[3])
                                query='insert into possiblecandidate values (%s, %s, %s, %s)'
                                ex(query, data)
                                con.commit()
                                print("Candidate application accepted")
                                input("\nPress Enter to go back to Candidate Registration Portal")
                                break
                            except:
                                print("Duplicate entry is not allowed")
                                input("\nPress Enter to go back to Candidate Registration Portal")
                                break
                        else:
                            print("Please enter correct PIN")
                            break
                else:
                    print("Your Candidate application was rejected.")
                    print("Please register as a permanent candidate first.")
            elif n=='3':
                break
            else:
                print("Please enter valid choice of action")
                
def candidateeligibility():
    from tabulate import tabulate
    ex('select * from possiblecandidate')
    t=cur.fetchall()
    if len(t)!=0:
        while True:
            n=input(("\n1. Select candidates for this election" \
            "\n2. Go Back to Admin Portal" \
            "\nEnter the choice of action:"))
            if n=='1':
                ex("use election")
                ex("delete from candidate")
                print("\n==============CANDIDATE SELECTION PORTAL==============")
                ex("use election")
                ex("select * from possiblecandidate")
                candidates=cur.fetchall()
                for i in range(len(candidates)):
                    j=candidates[i]
                    table=[{"Sl No.":i+1, "CandidateID":j[0], "Name":j[1], "DOB":j[2]}]
                    print("\n"+tabulate(table, headers="keys"))                    
                    n=input("Would you like to select this candidate (y/n)?:")
                    if n in "Yy":
                        ex("use election")
                        data=(j[0], j[1], j[2], j[3], 0)
                        query='insert into candidate values (%s, %s, %s, %s, %s)'
                        ex(query, data)
                        con.commit()
                        print("Candidate added to election list")
            elif n=='2':
                break
            else:
                print("Please enter valid choice of action")
    else:
        print("No candidates have registered for this election")
        print("Please ask candidates to register for this election before selecting candidates")

def admin():
    with open("metadata.txt","r") as f1:
        f1.readline()
        f1.readline()
        admin_password1=(f1.readline()).strip("\n")
    import sys
    import pwinput
    if sys.stdin.isatty():    
        ch=pwinput.pwinput(prompt='\nEnter Admin password:', mask='*')
    else:
        ch=input('\nEnter Admin password:')
    if ch==admin_password1:
        while True:
            print("\n==============ADMIN PORTAL==============")
            n=input("\n1. Approve Possible Voters" \
            "\n2. Approve Possible Candidates" \
            "\n3. Go Back to Configuration Portal" \
            "\nEnter the choice of action:")
            if n=='1':
                votereligibility()
            elif n=='2':
                candidateeligibility()
            elif n=='3':
                break
            else:
                print("Please enter valid choice of action")
    else:
        print("Incorrect Password. Admin privileges denied.")
        input("\nPress Enter to go back to Configuration Portal")

def programexit():
    with open("metadata.txt","r") as f1:
        f1.readline()
        f1.readline()
        admin_password1=(f1.readline()).strip("\n")
    import sys
    import pwinput
    if sys.stdin.isatty(): 
        ch=pwinput.pwinput(prompt='\nEnter Admin password:', mask='*')
    else:
        ch=input('\nEnter Admin password:')
    if ch==admin_password1:
        import subprocess
        print("\n==============EXIT PROGRAM OPTIONS==============")
        flag=True
        while flag:
            n=input("\n1. Delete Permanent Voter and Candidate Records" \
            "\n2. Delete Current Election Records" \
            "\n3. Exit the Program" \
            "\n4. Go Back to Configuration Portal" \
            "\nEnter the choice of action:")
            if n=='1':
                ex('use votebase')
                ex('delete from voter')
                ex('delete from candidate')
                print("Permanent Voter and Candidate Records Deleted")
                flag=True
                con.commit()
            elif n=='2':
                ex('use election')
                ex('delete from voter')
                ex('delete from candidate')
                ex('delete from possiblevoter')
                ex('delete from possiblecandidate')
                print("Current Election Records Deleted")
                flag=True
                con.commit()                         
            elif n=='3':
                import os
                os.remove("metadata.txt")
                print("Thanks for using VoterBase")
                input("Press Enter to exit the program")
                import sys
                sys.exit()
            elif n=='4':
                break
            else:
                print("Please enter valid choice of action")
                flag=True
    else:
        print("Incorrect Password. Admin privileges denied.")
        input("\nPress Enter to go back to Configuration Portal")

        
def finalreview():
    from tabulate import tabulate
    print("\n==============VOTERS==============")
    ex("use election")
    ex("select * from voter")
    voter=cur.fetchall()
    tablelist=[]
    for i in range(len(voter)):
        j=voter[i]
        table={"Sl No.":i+1, "VoterID":j[0], "Name":j[1], "DOB":j[2]}
        tablelist.append(table)
    print("\n"+tabulate(tablelist, headers="keys"))
    print("\n")
    print("\n==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    tablelist1=[]
    for i in range(len(candidates)):
        j=candidates[i]
        table1={"Sl No.":i+1, "CandidateID":j[0], "Name":j[1], "DOB":j[2]}
        tablelist1.append(table1)
    print("\n"+tabulate(tablelist1, headers="keys"))
    ch=input("Would you like to remove Voters or Candidates (y/n)?:")    
    while ch in "Yy":
        ch1=input("\n1. Remove Voters \
                  \n2. Remove Candidates" \
                  "\nEnter the choice of action:")
        if ch1=='1':
            id=input("Enter VoterID to remove:")
            query='delete from voter where VoterID=%s'
            data=(id,)
            ex(query,data)
            con.commit()
        elif ch1=='2':
            id=input("Enter CandidateID to remove:")
            query='delete from candidate where CandidateID=%s'
            data=(id,)
            ex(query,data)
            con.commit()
        else:
            print("Please enter valid choice of action")
        ch=input("Would you like to continue editing the voter and candidate lists (y/n)?:")
    print("\n==============VOTERS==============")
    ex("use election")
    ex("select * from voter")
    voter=cur.fetchall()
    tablelist=[]
    for i in range(len(voter)):
        j=voter[i]
        table={"Sl No.":i+1, "VoterID":j[0], "Name":j[1], "DOB":j[2]}
        tablelist.append(table)
    print("\n"+tabulate(tablelist, headers="keys"))
    print("\n")
    print("\n==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    tablelist1=[]
    for i in range(len(candidates)):
        j=candidates[i]
        table1={"Sl No.":i+1, "CandidateID":j[0], "Name":j[1], "DOB":j[2]}
        tablelist1.append(table1)
    print("\n"+tabulate(tablelist1, headers="keys"))
    input("Press Enter to go to election portal")            

def main():
    while True:
        print("\n==============CONFIGURATION PORTAL==============")
        n=input("\n1. Voter\n2. Candidate\n3. Admin\n4. Go To Election Portal\n5. Exit" \
        "\nEnter the choice of action:")
        if n=='1':
            voterregister()
        elif n=='2':
            candidateregister()
        elif n=='3':
            admin()
        elif n=='4':
            n=input("\n1. Review Voter and Candidate Lists before Starting Election" \
            "\n2. Skip Review and Go To Election Portal" \
            "\nEnter the choice of action:")
            if n=='1':
                finalreview()
                import elections
                elections.electionportal()
            elif n=='2':
                import elections
                elections.electionportal()
            else:
                print("Please enter valid choice of action")
        elif n=='5':
            programexit()
        else:
            print("Please enter valid choice of action")

