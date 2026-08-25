import mysql.connector as sq

con=sq.connect(host='localhost', user='root', password='root')
cur=con.cursor()

def ex(x):
    cur.execute(x)

ex('create database votebase')
ex('use votebase')
ex('create table voter(VoterID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
ex('create table candidate(CandidateID varchar(10) primary key, Name varchar(50), DOB date, PIN varchar(4))')
