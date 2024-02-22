# Bashed
### 10.10.10.68

Let's run the normal Nmap scan:
```{r, engine='bash', count_lines}
> nmap -sC -sV 10.10.10.68

Starting Nmap 7.60 ( https://nmap.org ) at 2017-12-19 06:52 EST
Nmap scan report for 10.10.10.68
Host is up (0.073s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.31 seconds
```

as we can see, the only thing running is an Apache web server, and if we browse to it, we see a little blog, although its only HTML so it doesn't seem like an attack vector, what we do see, is that the blog is talking about a product called "phpbash" made by the blog's owner which is a php based shell, and not only that, he is saying he developed the product on this server, interesting... is it possible for us to find and access that php based shell to get access to the machine? i guessed a couple folder names like development and devel, and on the third try i found it! theres a folder called dev! and not only that it contains the phpbash script inside it! and if we run it (10.10.10.68/dev/phpbash.php) we get a basic shell!

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/phpbash.png "phpbash")

and if we check for a user.txt...

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Jeeves/images/user.png "user")

we get the user hash!
