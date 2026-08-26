import csv
import mysql.connector as sq

con = sq.connect(host='localhost', user='root', password='root')
cur = con.cursor()

def encode(num):
    l=['a' , '?' , '$' , 'C' , 'j' , '+' , '@' , 'q' , '%' , '<']
    s=''
    for i in str(num):
        s+=l[int(i)]
    return s

def decode(s):
    l=['a' , '?' , '$' , 'C' , 'j' , '+' , '@' , 'q' , '%' , '<']
    num=''
    for i in s:
        for k in l:
            if i==k:
                num+=str(l.index(k))
    return num

def ex(x, values=None):
    if values is not None:
        cur.execute(x, values)
    else:
        cur.execute(x)


def initialise():
    try:
        ex('create database election')
        ex('use election')
        ex('create table voter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Voted varchar(3) default "NO")')
        ex('create table candidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4), Votes int default 0)')
    except:
        pass

def resultstable():
    ex("use election")
    ex("select * from candidate")
    candidates = cur.fetchall()
    print("Sl No.\tCandidateID\tName\t\tDOB\tVotes Received")
    for i in range(len(candidates)):
        j = candidates[i]
        print(i+1, "\t", j[0], "\t\t", j[1], "\t", j[2], "\t", j[4])

#------------------------------voter portal--------------------------------
def VoterAdd():
    ex('use votebase')
    ex('select * from voter')
    voter = cur.fetchall()
    vid = input('Enter your Voter ID: ')
    found = False
    for i in voter:
        if i[0] == vid:
            found = True
            pin = input('Enter your PIN: ')
            if pin.isdigit() and len(pin) == 4 and decode(i[3]) == pin:
                ex('use election')
                ex('select VoterID from voter where VoterID = %s', (vid,))
                existing = cur.fetchone()
                if existing:
                    print('Voter is already registered in this election!')
                else:
                    print('Voter has been verified...')
                    ex('insert into voter values(%s,%s,%s,%s,%s)', (i[0], i[1], i[2], i[3], 'NO'))
                    con.commit()
                    print('Registered for the election...')
            else:
                print('Wrong PIN')
            break
    if not found:
        print('Invalid Voter ID')

def vote():
    ex('use election')
    ex('select * from voter')
    voter = cur.fetchall()
    ex('select CandidateID, Name from candidate')
    candidates = cur.fetchall()
    if not candidates:
        print('No candidates available to vote for.')
        return
    vid = input('Enter your Voter ID: ')
    found = False
    for i in voter:
        if i[0] == vid:
            found = True
            pin = input('Enter your PIN: ')
            if pin.isdigit() and len(pin) == 4 and decode(i[3]) == pin:
                if i[4] == 'YES':
                    print('You have already voted! Double voting is not allowed.')
                else:
                    print('Voting:')
                    print('Candidate No.\t\tCandidate ID\t\tName')
                    c = 1
                    for cand in candidates:
                        print(c, '\t\t', cand[0], '\t\t', cand[1])
                        c += 1
                    ch = input('Enter suitable candidate no. (VOTING): ')
                    if ch.isdigit() and int(ch) in range(1, c):
                        cid = candidates[int(ch)-1][0]
                        ex('update candidate set Votes = Votes + 1 where CandidateID = %s', (cid,))
                        ex('update voter set Voted = "YES" where VoterID = %s', (vid,))
                        con.commit()
                        print('Vote recorded successfully!')
                    else:
                        print('Invalid Candidate no.')
            else:
                print('Wrong PIN')
            break
    if not found:
        print('Wrong Voter ID or Voter not registered in election...')

#-----------------------------candidate portal-------------------------
def CandidateAdd():
    ex('use votebase')
    ex('select * from candidate')
    candidate = cur.fetchall()
    cid = input('Enter your Candidate ID: ')
    found = False
    for i in candidate:
        if i[0] == cid:
            found = True
            pin = input('Enter your PIN: ')
            if pin.isdigit() and len(pin) == 4 and decode(i[3]) == pin:
                ex('use election')
                ex('select CandidateID from candidate where CandidateID = %s', (cid,))
                existing = cur.fetchone()
                if existing:
                    print('Candidate is already registered in this election!')
                else:
                    print('Candidate has been verified...')
                    ex('insert into candidate values(%s,%s,%s,%s, 0)', (i[0], i[1], i[2], i[3]))
                    con.commit()
                    print('Registered as candidate for election...')
            else:
                print('Wrong PIN')
            break
    if not found:
        print('Invalid Candidate ID')

def status():
    ex('use election')
    ex('select * from candidate')
    candidates = cur.fetchall()
    cid = input('Enter Candidate ID: ')
    found = False
    for i in candidates:
        if i[0] == cid:
            found = True
            pin = input('Enter your PIN: ')
            if pin.isdigit() and len(pin) == 4 and decode(i[3]) == pin:
                ex('select * from candidate where CandidateID=%s', (cid,))
                candidate = cur.fetchall()
                print('Candidate ID\t\tName\t\tVotes')
                print(candidate[0][0], '\t\t', candidate[0][1], '\t\t', candidate[0][4])
            else:
                print('Wrong PIN')
            break
    if not found:
        print('Candidate ID not found')

#------------------------admin portal-----------------------------------------
def end_election():
    ex('use election')
    ch = input('\nAre you sure you want to end the current election? (Y/N): ')
    if ch.lower() != 'y':
        print('Election ending cancelled.')
        return
    ex('select CandidateID, Name, DOB, Votes from candidate')
    candidates = cur.fetchall()
    ex('select VoterID, Name, DOB, Voted from voter')
    voters = cur.fetchall()
    filename = input('Enter a name for the election archive: ')
    with open(filename + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ELECTION RESULTS'])
        w.writerow([])
        w.writerow(['CandidateID', 'Name', 'DOB', 'Votes'])
        for i in candidates:
            w.writerow(i)
        w.writerow([])
        w.writerow(['REGISTERED VOTERS'])
        w.writerow(['VoterID', 'Name', 'DOB', 'Voted'])
        for voter in voters:
            w.writerow(voter)
    ex('delete from voter')
    ex('delete from candidate')
    con.commit()
    print('Election has ended...')
    print('Election data saved to', filename + '.csv')

def results():
    import matplotlib.pyplot as plt
    filename = input('Enter the election archive name: ')
    try:
        with open(filename + '.csv', 'r', newline='') as f:
            rows = list(csv.reader(f))
        candidates = []
        votes = []
        start = False
        for i in rows:
            if i == ['CandidateID', 'Name', 'DOB', 'Votes']:
                start = True
                continue
            if start:
                if not i:
                    break
                candidates.append(i[1])
                votes.append(int(i[3]))
        plt.bar(candidates, votes)
        plt.xlabel('Candidates')
        plt.ylabel('Votes')
        plt.title('Election Results')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        print('Election archive not found.')

#------------------------administrative options------------------------------
def viewvoters():
    ex('use election')
    ex('select VoterID, Name, DOB, Voted from voter')
    voters = cur.fetchall()
    print('\n========== REGISTERED VOTERS ==========')
    if not voters:
        print('No voters registered.')
        return
    print('VoterID\t\tName\t\tDOB\t\tVoted')
    for i in voters:
        print(i[0], '\t\t', i[1], '\t', i[2], '\t', i[3])


def removevoter():
    ex('use election')
    vid = input('Enter the Voter ID to remove: ')
    ex('select VoterID, Name from voter where VoterID = %s', (vid,))
    voter = cur.fetchone()
    if voter:
        print('\nVoter found:', voter[1])
        confirm = input('Are you sure you want to remove this voter? (Y/N): ')
        if confirm.lower() == 'y':
            ex('delete from voter where VoterID = %s', (vid,))
            con.commit()
            print('Voter removed')
        else:
            print('Removal cancelled')
    else:
        print("Voter ID not found")


def viewcandidates():
    ex('use election')
    ex('select CandidateID, Name, DOB, Votes from candidate')
    candidates = cur.fetchall()
    print('\n========== PARTICIPATING CANDIDATES ==========')
    if not candidates:
        print('No candidates registered.')
        return
    print('CandidateID\tName\t\tDOB\t\tVotes')
    for i in candidates:
        print(i[0], '\t\t', i[1], '\t', i[2], '\t', i[3])


def removecandidate():
    ex('use election')
    cid = input('Enter the Candidate ID to remove: ')
    ex('select CandidateID, Name from candidate where CandidateID = %s', (cid,))
    candidate = cur.fetchone()
    if candidate:
        print('\nCandidate found:', candidate[1])
        confirm = input('Are you sure you want to remove this candidate? (Y/N): ')
        if confirm.lower() == 'y':
            ex('delete from candidate where CandidateID = %s', (cid,))
            con.commit()
            print('Candidate removed successfully')
        else:
            print("Removal cancelled.")
    else:
        print("Candidate ID not found.")

def administrative():
    while True:
        print('\n========== ADMINISTRATIVE OPTIONS ==========')
        print('1. View Registered Voters')
        print('2. Remove Voter')
        print('3. View Participating Candidates')
        print('4. Remove Candidate')
        print('5. Back')
        ch = input('Enter your choice: ')
        if ch in ['1', '2', '3', '4', '5']:
            ch = int(ch)
        else:
            print('Invalid Choice')
            continue

        if ch == 1:
            viewvoters()
        elif ch == 2:
            removevoter()
        elif ch == 3:
            viewcandidates()
        elif ch == 4:
            removecandidate()
        elif ch == 5:
            break

def votingportal():
    while True:
        print('\n========== ELECTION SYSTEM ==========\n')
        print('1. Admin')
        print('2. Voter')
        print('3. Candidate')
        print('4. Exit')
        ch = input('Enter your choice: ')
        if ch in ['1', '2', '3', '4']:
            ch = int(ch)
        else:
            print('Invalid Choice')
            continue
            
        if ch == 4:
            import sys
            print('Exiting from Election Portal...')
            sys.exit()
        
        elif ch == 1:
            pin = input('Enter admin PIN: ')
            if pin == 'password':
                print('Verified...\n')
                while True:
                    print('\n========== ADMIN PORTAL ==========\n')
                    print('1. Administrative Options')
                    print('2. End Current Election')
                    print('3. View Election Results')
                    print('4. Back to Main Menu')
                    ch = input('Enter your choice: ')
                    if ch in ['1', '2', '3', '4']:
                        ch = int(ch)
                    else:
                        print('Invalid Choice')
                        continue
                    if ch == 4:
                        break
                    elif ch == 1:
                        administrative()
                    elif ch == 2:
                        end_election()
                    elif ch == 3:
                        results()
                        resultstable()
            else:
                print('Incorrect Admin PIN')

        elif ch == 2:
            while True:
                print('\n========== VOTER PORTAL ==========\n')
                print('1. Register as Voter')
                print('2. Vote')
                print('3. Back to Main Menu')
                ch = input('Enter your choice: ')
                if ch in ['1', '2', '3']:
                    ch = int(ch)
                else:
                    print('Invalid Choice')
                    continue
                if ch == 3:
                    break
                elif ch == 1:
                    VoterAdd()
                elif ch == 2:
                    vote()

        elif ch == 3:
            while True:
                print('\n========== CANDIDATE PORTAL ==========\n')
                print('1. Register as Candidate')
                print('2. See Your Election Status')
                print('3. Back to Main Menu')
                ch = input('Enter your choice: ')
                if ch in ['1', '2', '3']:
                    ch = int(ch)
                else:
                    print('Invalid Choice')
                    continue
                if ch == 3:
                    break
                elif ch == 1:
                    CandidateAdd()
                elif ch == 2:
                    status()

initialise()
votingportal()
