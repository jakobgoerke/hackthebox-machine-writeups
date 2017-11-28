# Jeeves
#### 10.10.10.63

Let's run the normal Nmap scan:
```{r, engine='bash', count_lines}
> nmap -sC -sV 10.10.10.63

Nmap scan report for jeeves.htb (10.10.10.63)
Host is up (0.095s latency).
Not shown: 997 filtered ports
PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Ask Jeeves
135/tcp open  msrpc        Microsoft Windows RPC
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
Service Info: Host: JEEVES; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 5h00m05s, deviation: 0s, median: 5h00m05s
| smb-security-mode: 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2017-11-11 19:01:26
|_  start_date: 2017-11-11 19:01:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 59.48 seconds
```

we can see theres a webserver running (Microsoft IIS in this case, which is preinstalled on all windows server editions), after some basic enumeration on the webserver and just looking around there isnt much to it. so while we keep looking we ran a full tcp server in the background:
```{r, engine='bash', count_lines}
> nmap -p- -v 10.10.10.63

-snip-
Discovered open port 50000/tcp on 10.10.10.63
-snip-
```
aha! an open port, which seems to be a Jetty Servlet Server (basically a webserver for java), after some dirbustting we found the /askjeeves/ directory which has a full blown installtion of Jenkins(a popular automatic build server for java) and not only that, its completely open with no password! one of the main features of jeeves is alot of customization of those customization options is running arbitary commands before/after the build started/finished, which is just perfect for us!
so lets create a new project:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/createproject.png "createproject")

now lets create a new build action which will run a cmd command:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/addbuild.png "addbuild")

set the command to "whoami" just to test the command execution:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/whoami.png "whoami")

run the build proccess:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/buildnow.png "buildnow")

and success! we have command execution.

so now lets try to get the user.txt:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/userset.png "userset")

and lets test it:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/userget.png "userget")

GG! we have the user hash!

Now for the root.txt i would like to have a more interactive shell, as this proccess is kinda repetetive, the problem is, if we try to run any kind of powershell shell or meterpreter shell, we will see the built in windows defender is blocking it!
But do not fear! Veil is here for the rescue(Veil is a tool designed to evade several common antiviruses using metasploit modules), so after installing Veil, we can start it up and make the payload:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/veilinit.png "veilinit")

lets set LHOST and LPORT:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/veilset.png "veilset")

and create the payload using the "generate" command:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/veilgen.png "veilgen")

as we can see veil provides us with both the powershell payload and a nice metasploit script we can load with "msfconsole -r <file>" to automaticlly listen for the payload:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/msfcon.png "msfcon")

and then run the payload through jenkins:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/msfrun.png "msfrun")

and success! we have a meterpreter session, now lets interact with it using "sessions -i 1", and start poking around.

After sometime i stumbled upon the "CEH.kdbx" file in the Documents folder of the "kohsuke" user, if we run "file" on it we will find its a Keepass(opensource password manager) password database, so lets run johntheripper on it to try and get in. after a couple seconds john reports the password is "moonshine1". lets extract all of the passwords from that psdb using keepassdump.
alot of random passwords show up but one looks interesting:
```{r, engine='bash', count_lines}
BackupStuff
aad3b435b51404eeaad3b435b51404ee:e0fb1fb85756c24235ff238cbe81fe00
```
the password labled BackupStuff does not look like a password, but it does look like an NTLM hash(windows password hash), we can try to use one of the more famous exploits, pass the hash(pass the hash is a scenrio in which you give a program the hashed password instead of the password itself but still get in). Metasploit has a built in module for passthehash attacks, called "psexec".
lets run and configure psexec:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/admin.png "admin")

Great! we have an administrator shell, but oh no! there is no root.txt in the administrator desktop, only an empty file called hm.txt

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/hm.png "hm")

After some poking around we find that the file has a suspicous ntfs attribute(every file in an ntfs filesystem is made up of attributes, for example all of the data of the file is in the $DATA attribute) which is called root.txt! this type of attribute is called an alternate data stream, as its the smae as $DATA only it has a different name so when you read it, the software that reads the file doesnt display it. (you can check for ntfs alternate streams using the "Streams" program by microsoft: https://docs.microsoft.com/de-de/sysinternals/downloads/streams)
```{r, engine='dos', count_lines}
C:\Users\Administrator\Desktop>streams64.exe hm.txt
streams64.exe hm.txt

streams v1.60 - Reveal NTFS alternate streams.
Copyright (C) 2005-2016 Mark Russinovich
Sysinternals - www.sysinternals.com

C:\Users\Administrator\Desktop\hm.txt:
        :root.txt:$DATA	34
```

so lets try to extract that data stream using powershell:

```{r, engine='dos', count_lines}
C:\Users\Administrator\Desktop>powershell -c "Get-Content -Path c:\users\administrator\desktop\hm.txt -Stream root.txt"
powershell -c "Get-Content -Path c:\users\administrator\desktop\hm.txt -Stream root.txt"
afbc5bd4b615a60648cec41c6ac92530
```

Success! we have rooted the machine.