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

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/userget.png "userget")

and lets test it:

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/userset.png "userset")

GG! we have the user hash!
