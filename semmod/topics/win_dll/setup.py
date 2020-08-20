#!/usr/bin/python
import sys, commands, os


if sys.platform == 'cygwin':

  cmd = "gcc --shared cokus.c topics.c -o topics.dll"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

elif sys.platform == 'linux2':
  fPIC = ''
  if os.uname()[4].find("_64") > 0:
    fPIC = " -fPIC"

  cmd = "gcc -c topics.c%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "ld -shared topics.o -o topics.so"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status
