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

def voting():
    ch='y'
    while ch in "Yy":
        ex("use election")
        ex("select * from candidate")
        candidates=cur.fetchall()
        print("Sl No.\tCandidateID\tName\tDOB")
        for i in range(len(candidates)):
            j=candidates[i]
            print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
        n=int(input("Enter your choice of candidate (as number):"))
        if n<=len(candidates):
            ex("select * from candidate") #Selecting Candidate Tuple
            value=cur.fetchall()
            c=value[n-1]
            ex("select Votes from candidate") #Selecting originial vote count
            votevalue=cur.fetchall()
            votecount=votevalue[n-1][0]
            ex("select CandidateID from candidate") #Selecting Candidate ID
            votecandidate=cur.fetchall()
            votecandidateid=votecandidate[n-1][0]
            sql="update candidate set votes = %s where CandidateID = %s"
            val=(votecount+1, votecandidateid)
            ex(sql,val) #Updating vote count
            con.commit()
        else:
            print("Please enter valid candidate number")
        ch=input('Would you like to continue the election (y/n)?:')

def candidateeligibility():
    ex("use votebase")
    ex("select * from candidate")
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

def votereligibility():
    ex("use votebase")
    ex("select * from voter")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2])
        n=input("Would you like to select this voter (y/n)?:")
        if n in "Yy":
            ex("use election")
            data=(j[0], j[1], j[2], j[3])
            query='insert into voter values (%s, %s, %s, %s)'
            ex(query, data)
            con.commit()
            print("Voter added to electoral rolls")

def resultstable():
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB\tVotes Received")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2],"\t",j[4])

def programexit():
    ex('use election')
    ex('delete from voter')
    ex('delete from candidate')
    con.commit()
    import sys
    sys.exit()

def votingportal():
    ch='y'
    while ch in "Yy":
        n=int(input('\n1. Add Voters to Participate in this Election' \
        '\n2. Add Candidates to Participate in this Election' \
        '\n3. Start Election' \
        '\n4. Display Results in Table Format' \
        '\n5. Exit' \
        '\nEnter the choice of action:'))
        if n==1:
            votereligibility()
        elif n==2:
            candidateeligibility()
        elif n==3:
            voting()
        elif n==4:
            resultstable()
        elif n==5:
            programexit()


initialise()
votingportal()



        
            