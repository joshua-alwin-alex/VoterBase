import mysql.connector as sq

con=sq.connect(host='localhost', user='root', password='root')
cur=con.cursor()

def ex(x,values=None):
    cur.execute(x,values)

def initialise():
    try:
        ex('create database election')
        ex('use election')
        ex('create table voter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Voted varchar(10))')
        ex('create table candidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Votes int)')
        ex('create table possiblevoter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
        ex('create table possiblecandidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
    except:
        pass

def voterregister():
    id=input("Enter VoterID:")
    pin=int(input("Enter PIN:"))
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

def votereligibility():
    ex("use election")
    ex("select * from possiblevoter")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
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
    id=int(input("Enter CandidateID:"))
    pin=int(input("Enter PIN:"))
    ex('use votebase')
    ex("select * from candidate")
    voters=cur.fetchall()
    for i in voters:
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

def candidateeligibility():
    ex("use election")
    ex("select * from possiblecandidate")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
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
    n=int(input("\n1. Approve Possible Voters" \
    "\n2. Approve Possible Candidates"))
    if n==1:
        votereligibility()
    elif n==2:
        candidateeligibility()

def programexit():
    ex('use election')
    ex('delete from voter')
    ex('delete from candidate')
    con.commit()
    import sys
    sys.exit()

def main():
    while True:
        n=int(input("\n1. Voter\n2. Candidate\n3. Admin\n4. Go To Election Portal\n5. Exit" \
        "\nEnter the choice of action:"))
        if n==1:
            voterregister()
        elif n==2:
            candidateregister()
        elif n==3:
            admin()
        elif n==4:
            import elections
            elections.votingportal()
        elif n==5:
            programexit()

initialise()
main()
        


