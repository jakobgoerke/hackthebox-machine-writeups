# Blocky

##### 10.10.10.37

## NMAP SCAN [intensive scan]

![nmap scan](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Blocky/images/nmap.png "NMAP Scan")

Lets visit the website.
![index.php](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Blocky/images/index.png "index.php")
After doing some basic enumeration, we see that it is a Wordpress Website and a directory called /plugins.
![/plugins](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Blocky/images/plugins.png "10.10.10.37/plugins")

Let's download the BlockyCore.jar and extract it.
We see, theres a blockycore.class, which could get interesting.
And yes, it is indeed interesting. After running **strings** on it, we see something really juicy:

![strings](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Blocky/images/strings.png "strings blockycore.class")

We should test if these are the credentials for **phpmyadmin**.
And yes, they are.

![awesome](http://i.memeful.com/media/post/ewYyqmw_700wa_0.gif)

Okay. Keep calm and pwn. Let's see what the wpusers database is about.

![notch](https://github.com/jakobgoerke/HTB-Writeups/blob/master/Blocky/images/notch.png)
Who that could be.. Maybe the ssh user?!
![batman](http://i.memeful.com/media/post/4wbB3ow_700wa_0.gif)
