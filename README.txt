To install on Linux:
Open a terminal, and enter the following commands.
> sudo python setup.py install


To install on Windows:
Use **win** directory
Open the Windows command line prompt and navigate to the semmod-1.7 directory
> cd [your path]\semmod-1.7
Then enter this command:
> python setup.py install


Running 64-bit Linux?
By default SEMMOD comes with C modules compiled for 32-bit Linux systems. If you are running a 64-bit system then you will need to run the setup.py scripts in the following directories with the command line "python setup.py":

  [your install directory]/semmod-1.7/semmod/spsvd/setup.py
  [your install directory]/semmod-1.7/semmod/csm/setup.py
  [your install directory]/semmod-1.7/semmod/spnmf/setup.py
  [your install directory]/semmod-1.7/semmod/topics/setup.py

Note: Do this before you run the main installation script contained in:

  [your install directory]/semmod-1.1/setup.py


Running 64-bit Windows?
By default SEMMOD comes with C modules compiled for 32-bit Windows systems. To get better performance from your 64-bit system, copy the following files to the designated directories:

  [your install directory]/semmod-1.7/semmod/spsvd/64/spsvd/_spsvd.dll -> [your install directory]/semmod-1.7/semmod/spsvd/_spsvd.dll
  [your install directory]/semmod-1.7/semmod/csm/64/csm/_csm.dll -> [your install directory]/semmod-1.7/semmod/csm/_csm.dll
  [your install directory]/semmod-1.7/semmod/spnmf/64/spnmf/_spnmf.dll -> [your install directory]/semmod-1.7/semmod/spnmf/_spnmf.dll
  [your install directory]/semmod-1.7/semmod/topics/64/topics/_topics.dll -> [your install directory]/semmod-1.7/semmod/topics/_topics.dll  

Note: On Windows systems, 32-bit libraries will also run on 64-bit systems.






 



