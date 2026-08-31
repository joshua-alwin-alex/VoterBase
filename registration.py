def installrequirements():
    import sys
    import subprocess
    try:
        import matplotlib
    except ImportError:
        print("Installing module matplotlib")
        try:    
            subprocess.run([sys.executable,"-m","pip","install","matplotlib"], check=True)
        except:
            subprocess.run([sys.executable,"-m","pip3","install","matplotlib"], check=True)
        finally:
            print("Successfully installed matplotlib")
    try:
        import numpy
    except:
        print("Installing module numpy")
        try:    
            subprocess.run([sys.executable,"-m","pip","install","numpy"], check=True)
        except:
            subprocess.run([sys.executable,"-m","pip3","install","numpy"], check=True)
        finally:
            print("Successfully installed numpy")
    try:
        import mysql.connector
    except:
        print("Installing module mysql.connector")
        try:    
            subprocess.run([sys.executable,"-m","pip","install","mysql.connector"], check=True)
        except:
            subprocess.run([sys.executable,"-m","pip3","install","mysql.connector"], check=True)
        finally:
            print("Successfully installed mysql.connector")        
        
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
            
            ex('use votebase')
            ex("select * from voter")
            voters=cur.fetchall()
            for i in voters:
                if i[0]==id and i[3]==pin:
                    ex("use election")
                    data=(i[0], i[1], i[2], i[3])
                    query='insert into possiblevoter values (%s, %s, %s, %s)'
                    ex(query, data)
                    con.commit()
                    print("Voter application accepted")
                    break
            else:
                print("Your Voter application was rejected")
        elif n=='3':
            break
        else:
            print("Please enter valid choice of action")

def votereligibility():
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
                candidates=cur.fetchall()
                for i in range(len(candidates)):
                    print("\nSl No.\tCandidateID\tName\tDOB")
                    j=candidates[i]
                    print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
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
                ex('use votebase')
                ex("select * from candidate")
                candidate=cur.fetchall()
                for i in candidate:
                    if i[0]==id and i[3]==pin:
                        ex("use election")
                        data=(i[0], i[1], i[2], i[3])
                        query='insert into possiblecandidate values (%s, %s, %s, %s)'
                        ex(query, data)
                        con.commit()
                        print("Candidate application accepted")
                        break
                else:
                    print("Your Candidate application was rejected")
            elif n=='3':
                break
            else:
                print("Please enter valid choice of action")
                
def candidateeligibility():
    ex('select * from possiblevoter')
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
                    print("\nSl No.\tCandidateID\tName\tDOB")
                    j=candidates[i]
                    print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
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
    password='password'
    ch=input("Enter Admin password:")
    if ch==password:
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


def programexit():
    print("==============EXIT PROGRAM OPTIONS==============")
    flag=True
    while flag:
        n=input("\n1. Delete Permanent Voter and Candidate Records" \
        "\n2. Delete Current Election Records" \
        "\n3. Exit the Program" \
        "\nEnter the choice of action:")
        if n=='1':
            ex('drop database votebase')
            print("Permanent Voter and Candidate Records Deleted")
            flag=True
            con.commit()
        elif n=='2':
            ex('drop database election')
            print("Current Election Records Deleted")
            flag=True
            con.commit()            
        elif n=='3':
            print("Thanks for using VoterBase")
            import sys
            sys.exit()
        else:
            print("Please enter valid choice of action")
            flag=True
        
def finalreview():
    print("\n==============VOTERS==============")
    ex("use election")
    ex("select * from voter")
    voter=cur.fetchall()
    print("\nSl No.\tVoterID\tName\tDOB")
    for i in range(len(voter)):
        j=voter[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    print("\n")
    print("\n==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("\nSl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
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
    print("\nSl No.\tVoterID\tName\tDOB")
    for i in range(len(voter)):
        j=voter[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    print("\n")
    print("\n==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("\nSl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
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

installrequirements()
import mysql.connector as sq
from permanent import *
con=sq.connect(host='localhost', user='root', password='root')
cur=con.cursor()
initialise()
main()