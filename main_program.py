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

def installrequirements():
    print("\n==============INSTALLING REQUIREMENTS==============")
    import sys
    import subprocess

    try:
        import windows_tools.installed_software
        print("\n1. windows_tools.installed_software is already installed")
    except:
        try:
            cmd=["pip","install","windows_tools.installed_software"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("\n1. windows_tools.installed_software successfully installed")
        except:
            cmd=["pip3","install","windows_tools.installed_software"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("\n1. windows_tools.installed_software successfully installed")            

    from windows_tools.installed_software import get_installed_software
    for software in get_installed_software():
        if "mysql" in software['name'].lower():
            print("2. MySQL is already installed")
            break
    else:
        print("Please install MySQL before running the application")
        import os
        os.remove("metadata.txt")
        input("\nPress Enter to exit the program")
        sys.exit()

    try:
        import pwinput
        print("3. pwinput is already installed")
    except:
        try:
            cmd=["pip","install","pwinput"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("3. pwinput successfully installed")
        except:
            cmd=["pip3","install","pwinput"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("3. pwinput successfully installed")

    try:
        import numpy
        print("4. numpy is already installed")
    except:
        try:
            cmd=["pip","install","numpy"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("4. numpy successfully installed")
        except:
            cmd=["pip3","install","numpy"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("4. numpy successfully installed")

    try:
        import matplotlib
        print("5. matplotlib is already installed")
    except:
        try:
            cmd=["pip","install","matplotlib"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("5. matplotlib successfully installed")
        except:
            cmd=["pip3","install","matplotlib"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("5. matplotlib successfully installed")

    try:
        import mysql.connector
        print("6. mysql.connector is already installed")
    except:
        try:
            cmd=["pip","install","mysql.connector"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("6. mysql.connector successfully installed")
        except:
            cmd=["pip3","install","mysql.connector"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("6. mysql.connector successfully installed")  

    try:
        import tabulate
        print("7. tabulate is already installed")      
    except:
        try:
            cmd=["pip","install","tabulate"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("7. tabulate successfully installed")
        except:
            cmd=["pip3","install","tabulate"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("7. tabulate successfully installed")

    try:
        import PIL
        print("8. pillow is already installed")      
    except:
        try:
            cmd=["pip","install","tabulate"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("8. pillow successfully installed")
        except:
            cmd=["pip3","install","tabulate"]
            process=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            code=process.wait()
            if code==0:
                print("8. pillow successfully installed")

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


    elif c.lower() == "show conditions clause":
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

    installrequirements()

    print("\n==============MYSQL LOGIN==============")
    import sys
    import pwinput
    if sys.stdin.isatty():    
        username=input("Enter your MySQL username:")
        password=pwinput.pwinput(prompt='Enter your MySQL password:', mask='*')
    else:
        username=input("Enter your MySQL username:")
        password=input("Enter your MySQL password:")

    print("\n==============SET ADMIN PASSWORD==============")
    import sys
    import pwinput
    if sys.stdin.isatty():    
        admin_password=pwinput.pwinput(prompt='Set your Admin password:', mask='*')
    else:
        admin_password=input("Set your Admin password:")


    with open("metadata.txt","w") as f1:
        login=[username,"\n"+password, "\n"+admin_password]
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
    initialise()
    main()
