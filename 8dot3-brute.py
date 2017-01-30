#!/usr/bin/python
# 8dot3-brute.py
# Script to attempt to guess filenames and directories from Windows 8.3 names. 
# Only useful if we are bruteforcing a relatively small character space.
# Always limit your character set (Ex. -c 'ABC12345' ) when possible. 
#
# References:
# https://github.com/irsdl/IIS-ShortName-Scanner
#
# Author: Paulino Calderon <paulino@calderonpale.com>

from itertools import product
from string import printable
import urllib
import requests
import sys, getopt

def banner():
  print("Usage: %s -u <base url> -f <filename> -d <dirname> -l <length> -c <character set>" % sys.argv[0])
  print("Usage: %s -u http://example.com -d 'DOCUME' -v" % sys.argv[0])
  print("Usage: %s -u http://example.com -f 'BACKU.ZIP' -c 'P0123456789' -v" % sys.argv[0])
  print("Usage: %s -u http://example.com -d 'DOCUME' -c 'NTOS' -v" % sys.argv[0])
  print("Usage: %s -u http://example.com -d 'DOCUME' -l 3 -v" % sys.argv[0])

#Valid 8.3 characters for files
def get_charset():
  return "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%&'()-@^_`{}~ "

def req(url):
  if debug:
    print "Trying '%s'" % (url)
  r = requests.get(file_url)
  #Only show responses different to 404 and 400
  if r.status_code != 404 and r.status_code != 400:
    print "%s STATUS:%s LENGTH:%s" % (file_url, r.status_code, len(r.text))

shortfilename = ''
dirname = ''
ext = ''
host = ''
char_max = 4
debug = False
charset = get_charset()

try:
  opts, args = getopt.getopt(sys.argv[1:],"vu:l:f:d:c:")
  if not opts:
    banner()
    sys.exit(2)
except getopt.GetoptError as e:
  print (str(e))
  banner()
  sys.exit(2)

for o, a in opts:
    if o == '-f':
      shortfilename = a
    if o == '-d':
      dirname = a
    elif o == '-u':
      host = a
    elif o == '-l':
      char_max = a
    elif o == '-c':
      charset = a
    elif o == '-v':
      debug = True

if shortfilename:
  shortfilename = shortfilename.split(".")
  if len(shortfilename) < 2:
    banner()
    sys.exit(2)

  ext = shortfilename[1]
  shortfilename = shortfilename[0]

  if len(ext) < 3:
    print "Extensions must have 3 characters."
    sys.exit(2)

  for i in range(1,int(char_max)+1):
    for str in map(''.join, product(charset, repeat=i)):
      escaped_str = urllib.pathname2url(str)
      file_url = "%s/%s.%s" % (host, shortfilename + escaped_str, ext)
      req(file_url)
      if ext == "ASP":
        ext = "ASPX"
        req("%s/%s.%s" % (host, shortfilename + escaped_str, ext))
      if ext == "CON":
        ext = "CONFIG"
        req("%s/%s.%s" % (host, shortfilename + escaped_str, ext))
        ext = "CONF"
        req("%s/%s.%s" % (host, shortfilename + escaped_str, ext))

if dirname:
  for i in range(1,int(char_max)+1):
    for str in map(''.join, product(charset, repeat=i)):
      escaped_str = urllib.pathname2url(str)
      file_url = "%s/%s" % (host, dirname + escaped_str)
      req(file_url)


