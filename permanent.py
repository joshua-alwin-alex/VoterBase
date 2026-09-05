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

#voter and candidate info...

with open("metadata.txt","r") as f1:
    username=(f1.readline()).strip("\n")
    password=(f1.readline()).strip("\n")

from main_program import con,cur
from datetime import date

def ex(x,values=None):
    cur.execute(x,values)

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

def agecheck(y,m,d,verify=18):
    dob=date(y , m , d)
    today=date.today()
    age=today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age-=1
    return age>=verify

def voter():
    ex('use votebase')
    ex('select * from voter')
    rows=sorted(cur.fetchall())
    
    ch=1
    while ch:
            name=input('\nEnter voter name: ')
            dob=input('Enter date of birth (DD-MM-YYYY): ').split('-')
            try:
                d,m,y=dob
                dob=date(int(y),int(m),int(d))
            except (ValueError, TypeError):
                print('Invalid Date')
                continue
            if any((name, dob) == (i[1], i[2]) for i in rows):
                print('Voter already registered!')
                continue
            if agecheck(int(y),int(m),int(d)):
                print('Eligible to vote!')
                if not rows:
                    vid='V1001'
                else:
                    v=0
                    vid='V1001'
                    for i in rows:
                        if i[0]==vid:
                            v+=1
                            vid='V'+str(1000+v+1)
                print('\nNew Voter ID: ' , vid)
                p=input('Enter 4-digit PIN: ')
                if len(p)==4 and p.isdigit():
                    p=encode(p)
                    ex('insert into voter values(%s,%s,%s,%s)',(vid,name,dob,p))
                    con.commit()
                    print('Voter Information Added...')
                    ch=0
                    break
                else:
                    print('Wrong Pin')
            else:
                print('Not eligible to vote...')

def candidate():
    ex('use votebase')
    ex('select * from candidate')
    rows=sorted(cur.fetchall())
    ex('select * from voter')
    vrows=sorted(cur.fetchall())
    
    ch=1
    while ch:
            name=input('\nEnter candidate name: ')
            dob=input('Enter date of birth (DD-MM-YYYY): ').split('-')
            try:
                d,m,y=dob
                dob=date(int(y),int(m),int(d))
            except (ValueError, TypeError):
                print('Invalid Date')
                continue
            if any((name, dob) == (i[1], i[2]) for i in rows):
                print('Candidate already registered!')
                continue
            cit=input('Are you an Indian citizen? (Y/N):')
            if cit.lower()!='y':
                print('Not eligible to contest...')
                continue
            bar=input('Are you barred from contesting elections due to a criminal conviction? (Y/N): ')
            if bar.lower()!='n':
                print('Not eligible to contest...')
                continue
            vid=input('Enter your Voter ID (mandatory): ')
            if agecheck(int(y),int(m),int(d),25):
                if any((vid, name, dob)==(i[0],i[1],i[2]) for i in vrows):
                    print('Eligible to contest for elections!')
                    if not rows:
                        cid='C1001'
                    else:
                        c=0
                        cid='C1001'
                        for i in rows:
                            if i[0]==cid:
                                c+=1
                                cid='C'+str(1000+c+1)
                    print('\nNew Candidate ID: ' , cid)
                    p=input('Enter 4-digit PIN: ')
                    if len(p)==4 and p.isdigit():
                        p=encode(p)
                        ex('insert into candidate values(%s,%s,%s,%s)',(cid,name,dob,p))
                        con.commit()
                        print('Candidate Information Added...')
                        ch=0
                        break
                    else:
                        print('Wrong Pin')
                else:
                    print('Wrong Information Found')
            else:
                print('Not eligible to contest...')
