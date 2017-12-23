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

root@kali:~/hackthebox/Machines/Inception# searchsploit dompdf

| Exploit Title                                                   |  Path                       |
|:-------------------------:                                      |:-------------------------:  |
|TYPO3 ke DomPDF Extension - Remote Code Execution                | php/webapps/35443.txt       |
|dompdf 0.6.0 - 'dompdf.php' 'read' Parameter Arbitrary File Read | php/webapps/33004.txt       |
|dompdf 0.6.0 beta1 - Remote File Inclusion                       | php/webapps/14851.txt       |



Feelsgoodman




IMAGE:
<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Tally/images/Website.PNG"></kbd>


TABLE:

| IP                  | FQDN                        |
| -------------       |:-------------------------:  |
| 10.10.10.65:443     | calvin.ariekei.htb          |
| 10.10.10.65:443     | beehive.ariekei.htb         |
