import mysql.connector as sq

con=sq.connect(host='localhost', user='root', password='root')
cur=con.cursor()

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
        ex('create table possiblecandidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass

def voterregister():
    print("==============VOTER REGISTRATION PORTAL==============")
    id=input("Enter VoterID:")
    pin=int(input("Enter PIN:"))
    ex('use votebase')
    ex("select * from voter")
    voters=cur.fetchall()
    for i in voters:
        if i[0]==id and i[3]==str(pin):
            ex("use election")
            data=(i[0], i[1], i[2], i[3])
            query='insert into possiblevoter values (%s, %s, %s, %s)'
            ex(query, data)
            con.commit()
            print("Voter application accepted")
            break
    else:
        print("Your Voter application was rejected")

def votereligibility():
    print("==============VOTER SELECTION PORTAL==============")
    ex("use election")
    ex("select * from possiblevoter")
    candidates=cur.fetchall()
    for i in range(len(candidates)):
        print("Sl No.\tCandidateID\tName\tDOB")
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

def candidateregister():
    print("==============CANDIDATE REGISTRATION PORTAL==============")
    id=input("Enter CandidateID:")
    pin=int(input("Enter PIN:"))
    ex('use votebase')
    ex("select * from candidate")
    candidate=cur.fetchall()
    for i in candidate:
        if i[0]==id and i[3]==str(pin):
            ex("use election")
            data=(i[0], i[1], i[2], i[3])
            query='insert into possiblecandidate values (%s, %s, %s, %s)'
            ex(query, data)
            con.commit()
            print("Candidate application accepted")
            break
    else:
        print("Your Candidate application was rejected")

def candidateeligibility():
    print("==============CANDIDATE SELECTION PORTAL==============")
    ex("use election")
    ex("select * from possiblecandidate")
    candidates=cur.fetchall()
    for i in range(len(candidates)):
        print("Sl No.\tCandidateID\tName\tDOB")
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

def admin():
    print("==============ADMIN PORTAL==============")
    n=int(input("\n1. Approve Possible Voters" \
    "\n2. Approve Possible Candidates" \
    "\nEnter the choice of action:"))
    if n==1:
        votereligibility()
    elif n==2:
        candidateeligibility()

def programexit():
    ex('use election')
    ex('delete from voter')
    ex('delete from candidate')
    ex('delete from possiblevoter')
    ex('delete from possiblecandidate')    
    con.commit()
    import sys
    sys.exit()

def finalreview():
    print("==============VOTERS==============")
    ex("use election")
    ex("select * from voter")
    voter=cur.fetchall()
    print("Sl No.\tVoterID\tName\tDOB")
    for i in range(len(voter)):
        j=voter[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    print("\n", end="")
    print("==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    ch=input("Would you like to remove Voters or Candidates (y/n)?:")    
    while ch in "Yy":
        ch1=int(input("1. Remove Voters \
                  \n2. Remove Candidates" \
                  "\nEnter the choice of action:"))
        if ch1==1:
            id=input("Enter VoterID to remove:")
            query='delete from voter where VoterID=%s'
            data=(id,)
            ex(query,data)
            con.commit()
        elif ch1==2:
            id=input("Enter CandidateID to remove:")
            query='delete from candidate where CandidateID=%s'
            data=(id,)
            ex(query,data)
            con.commit()
        ch=input("Would you like to continue (y/n)?:")
    print("==============VOTERS==============")
    ex("use election")
    ex("select * from voter")
    voter=cur.fetchall()
    print("Sl No.\tVoterID\tName\tDOB")
    for i in range(len(voter)):
        j=voter[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    print("\n", end="")
    print("==============CANDIDATES==============")
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
    input("Press Enter to go to election portal")            

def main():
    while True:
        print("==============CONFIGURATION PORTAL==============")
        n=int(input("\n1. Voter\n2. Candidate\n3. Admin\n4. Go To Election Portal\n5. Exit" \
        "\nEnter the choice of action:"))
        if n==1:
            voterregister()
        elif n==2:
            candidateregister()
        elif n==3:
            admin()
        elif n==4:
            finalreview()
            import elections
            elections.electionportal()
        elif n==5:
            programexit()

initialise()
main()