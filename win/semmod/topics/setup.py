#!/usr/bin/python
import sys, commands, os


if sys.platform == 'cygwin':

  cmd = "gcc --shared cokus.c _topics.c -o _topics.dll"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

elif sys.platform == 'linux2':
  fPIC = ''
  if os.uname()[4].find("_64") > 0:
    fPIC = " -fPIC"

  cmd = "gcc -c _topics.c%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "ld -shared _topics.o -o _topics.so"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status
