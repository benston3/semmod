#!/usr/bin/env python

import sys
from distutils.core import setup
from distutils.sysconfig import get_python_lib
from distutils.dir_util import copy_tree
import os, platform

def installSubDirectories(packageName, directories, pythonLibPath):
  for dirs in directories:
    sourceDirectory = packageName + os.sep + dirs
    installDirectory = pythonLibPath + os.sep + packageName + os.sep + dirs
    copy_tree(sourceDirectory, installDirectory)

def copyFileError(directories, semmodPackage):
  print "Could not copy semmod sub directories to: ", semmodPackage
  print "You will need to manually copy the following sub directories to dist-packages/semmod:"
  for dirs in directories:
    print "semmod/%s" % dirs  

packageName = 'semmod'
ver = '1.6'
directories = ['spsvd', 'topics', 'spnmf', 'csm'] 
setup(name=packageName,
      version=ver,
      description= 'Semantic Models',
      author='Simon Dennis & Ben Stone',
      author_email='simon.dennis@gmail.com',
      url='http://mall.psy.ohio-state.edu/wiki/index.php/Semantic_Models_Package_(SEMMOD)',
      packages=[packageName]  
     )

copy_files = True
try:
  if (sys.argv[1].find('sdist') > -1) or (sys.argv[1].find('bdist') > -1):
    copy_files = False
except:
  pass

pythonLibPath = get_python_lib()

semmodPackage = os.path.join( pythonLibPath, packageName )
if copy_files:
  if os.path.isdir( semmodPackage ):
    installSubDirectories(packageName, directories, pythonLibPath)
  else:
    print "Library not in expected location"
    if platform.dist()[0] == 'Ubuntu':
      print "Trying Ubuntu specific solution"
      pythonLibPath = get_python_lib().replace('usr/lib','usr/local/lib')
      semmodPackage2 = os.path.join( pythonLibPath, packageName )
      if os.path.isdir( semmodPackage2 ):
        print "Found path on Ubuntu"
        installSubDirectories(packageName, directories, pythonLibPath)
      else:
        copyFileError(directories, semmodPackage2)
    else:
      copyFileError(directories, semmodPackage)




