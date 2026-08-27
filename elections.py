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
        ex('create table possiblecandidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Votes int)')
    except:
        pass

def voting():
    while True:
        ex("use election")
        ex("select Voted from voter")
        voted=cur.fetchall()
        for i in voted:
            if i[0]=="No":
                id=input("Enter VoterID:")
                pin=input("Enter PIN:")
                query="update voter set Voted = %s where VoterID = %s and PIN = %s"
                data=("Yes", id, pin)
                ex(query,data)
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
                break
        else:
            print("Election completed successfully")
            break
            

def resultstable():
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    print("Sl No.\tCandidateID\tName\tDOB\tVotes Received")
    for i in range(len(candidates)):
        j=candidates[i]
        print(i+1,"\t",j[0],"\t",j[1],"\t",j[2],"\t",j[4])

def saveresult():
    ex("use election")
    ex("select * from candidate")
    candidates=cur.fetchall()
    data=[]
    for i in candidates:
        data.append([i[0],i[1],i[2],i[4]])
    import csv
    ch=input("Enter the name of the csv file to save the result into:")
    with open(ch+".csv","w",newline='') as f1:
        w1=csv.writer(f1)
        w1.writerows(data)
    print("Election Result saved to",ch+".csv")

def resultsbarchart():
    import matplotlib.pyplot as plt
    import numpy as np
    ch=input("Enter the name of the png file to save the bar chart into:")
    ex("use election")
    ex("select * from candidate")
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
    plt.show()

def resultspiechart():
    import matplotlib.pyplot as plt
    import numpy as np
    ch=input("Enter the name of the png file to save the pie chart into:")
    ex("use election")
    ex("select * from candidate")
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
    plt.show()

def votingportal():
    for i in range(2):
        n=int(input('\n1. Start Election' \
        '\n2. Display Results in Table Format' \
        '\n3. Display Results in Bar Chart Format' \
        '\n4. Display Results in Pie Chart Format' \
        '\nEnter the choice of action:'))
        if n==1:
            voting()
        elif n==2:
            resultstable()
        elif n==3:
            resultsbarchart()
        elif n==4:
            resultspiechart()

if __name__=="__main__":
    initialise()
    votingportal()



        
            