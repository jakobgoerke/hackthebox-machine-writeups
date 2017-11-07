# Sneaky
#### 10.10.10.20

```{r, engine='bash', count_lines}
nmap 10.10.10.20

PORT   STATE SERVICE
80/tcp open  http
```

The website shows that its under construction

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/is_vuln_if.png "Is vuln if")


Dirbuster Initiate!

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/is_vuln_if.png "Is vuln if")

Well ofcourse, its under **dev**elopment

We are greeted by a Login screen

![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/is_vuln_if.png "Is vuln if")


Whats the autoresponse when we see a poorly made login page ?

Yes **' or '1' = '1**

Simple sql injection. Seems legit

After the login we get sjuicy stuff
![Alt test](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Shocker/images/is_vuln_if.png "Is vuln if")

Lets make a note of the info:

- name: admin
- name: thrasvilous
- RSA Private key
- We are No-one

Lets wget the RSA key

And because its a Private SSH key, we change its perms

```
root@kali:~/Hackthebox/Sneaky# wget http://10.10.10.20/dev/sshkeyforadministratordifficulttimes
--2017-11-07 17:24:48--  http://10.10.10.20/dev/sshkeyforadministratordifficulttimes
Connecting to 10.10.10.20:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1675 (1.6K)
Saving to: ‘sshkeyforadministratordifficulttimes’

sshkeyforadministratordifficulttimes  100%[=======================================================================>]   1.64K  --.-KB/s    in 0s      

2017-11-07 17:24:48 (120 MB/s) - ‘sshkeyforadministratordifficulttimes’ saved [1675/1675]

root@kali:~/Hackthebox/Sneaky# mv sshkeyforadministratordifficulttimes adminssh.key

root@kali:~/Hackthebox/Sneaky# chmod 600 adminssh.key 

```

**BUT!!!**

We dont have a port 22 (ssh) open on this box. Maybe it was setup on a different port.

Lets nmap all the ports 

After spending millions of years completing the nmap we see that there is no other port open.

![Alt test](https://media.giphy.com/media/l46CbAuxFk2Cz0s2A/giphy.gif)


Hold up! we found something else though

Port 161

Investigate Further

```
nmap -sS -sU -p 161 -T4 -A 10.10.10.20





```

**_shellz_**
