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

if __name__=="__main__":  
    print("""\nVoterBase v1.0.0, Copyright \u00a9 2026 Nandan B. Nair and Joshua Alwin Alex""")
    print("""VoterBase comes with ABSOLUTELY NO WARRANTY; for details type 'show warranty clause'.""")
    print("""This is free software, and you are welcome to redistribute it""")
    print("""under certain conditions; type `show conditions clause' for details.""")

    c=input("\nType command or press Enter to continue:")

    if c.lower() == "show warranty clause":
        print("""\nTHERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY""")
        print("""APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT""")
        print("""HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY""")
        print("""OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,""")
        print("""THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR""")
        print("""PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM""")
        print("""IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF""")
        print("""ALL NECESSARY SERVICING, REPAIR OR CORRECTION.""")
        print("\nProceeding with application...")


    elif c.lower == "show conditions clause":
        print("""\nThis program is free software: you can redistribute it and/or modify""")
        print("""it under the terms of the GNU General Public License as published by""")
        print("""the Free Software Foundation, either version 3 of the License, or""")
        print("""(at your option) any later version.""")
        print()
        print("""This program is distributed in the hope that it will be useful,""")
        print("""but WITHOUT ANY WARRANTY; without even the implied warranty of""")
        print("""MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the""")
        print("""GNU General Public License for more details.""")
        print("\nProceeding with application...")

    elif c=='':
        pass

    else:
        print("Invalid choice of action. Proceeding with application...")

    print("\n==============MYSQL LOGIN==============")
    username=input("Enter your MySQL username:")
    password=input("Enter your MySQL password:")


    with open("metadata.txt","w") as f1:
        login=[username,"\n"+password]
        f1.writelines(login)



if __name__=="__main__":
    import mysql.connector as sq
    con=sq.connect(host='localhost', user=username, password=password)
    cur=con.cursor()
else:
    with open("metadata.txt","r") as f1:
        username1=(f1.readline()).strip("\n")
        password1=(f1.readline()).strip("\n")
    import mysql.connector as sq
    con=sq.connect(host='localhost', user=username1, password=password1)
    cur=con.cursor()


if __name__=="__main__":
    from registration import *
    installrequirements()
    initialise()
    main()
