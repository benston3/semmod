#!/usr/bin/python
import sys, commands, os


if sys.platform == 'cygwin':

  cmd = "gcc --shared _csm.c -o _csm.dll"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

elif sys.platform == 'linux2':
  fPIC = ''
  if os.uname()[4].find("_64") > 0:
    fPIC = " -fPIC"

  cmd = "gcc -c _csm.c%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "ld -shared _csm.o -o _csm.so"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status
