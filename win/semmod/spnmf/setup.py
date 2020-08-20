#!/usr/bin/python
import sys, commands, os


if sys.platform == 'cygwin':

  cmd = "gcc _spnmf.c -o _spnmf.dll"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

elif sys.platform == 'linux2':
  fPIC = ''
  if os.uname()[4].find("_64") > 0:
    fPIC = " -fPIC"

  cmd = "gcc -c _spnmf.c%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "ld -shared _spnmf.o -o _spnmf.so"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status
