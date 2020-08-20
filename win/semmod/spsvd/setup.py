#!/usr/bin/python2.5
import sys, commands, os

PYTHON_VERSION = "python%d.%d" % (sys.version_info[0],sys.version_info[1])
PYTHON_INCLUDE = "/usr/include/%s" % PYTHON_VERSION

if sys.platform == 'cygwin':
  cmd = "gcc -I%s -L/lib/%s/config --shared _spsvd.c las2.c svdlib.c svdutil.c -l%s -o _spsvd.dll" % (PYTHON_INCLUDE, PYTHON_VERSION, PYTHON_VERSION)
  status, ans = commands.getstatusoutput(cmd)

elif sys.platform == 'linux2':
  fPIC = ''
  if os.uname()[4].find("_64") > 0:
    fPIC = " -fPIC"

  cmd = "gcc -c las2.c svdlib.h svdutil.h%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "gcc -c svdlib.c svdlib.h%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "gcc -c svdutil.c svdutil.h%s" % fPIC
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "gcc -c _spsvd.c svdlib.h -I%s%s" % (PYTHON_INCLUDE, fPIC)
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status

  cmd = "ld -shared _spsvd.o las2.o svdutil.o svdlib.o -o _spsvd.so"
  status, ans = commands.getstatusoutput(cmd)
  print cmd, status
