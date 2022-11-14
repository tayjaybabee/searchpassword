# searchpassword
Rapidly check offline if your password is in the compromized passwords list

In order to use this, first obtain the list of hashes of compromized passwords from [https://haveibeenpwned.com/Passwords](https://haveibeenpwned.com/Passwords)

Get the latest one that is the SHA-1 format in order by hash.  Currently, the latest one is Version 8.  It is a 36 GB text file which comes compressed down to a 16 GB 7-zip file for download.  Extract the text file from the downloaded 7-zip file into this project's working directory.

This 36 GB file is pretty large, takes up a lot of disk space, and takes a long time to scan through it looking for a particular password hash, so before you run searchpass.py for the first time, run index_hashfile.py which creates a .yaml file that is an index of the large text file.  It figures out the locations of 4096 segments of the large text file so that later searchpass.py can seek directly to that segment and search through the hash list of only that section.  The index file is in yaml format and takes up 217 kB.  Each of the 4096 segments that it will search through is about 9 MB.

This may be modified to create a larger index and smaller segments to search through, eg. 3.4 MB index for 500 kB segments.  It will take longer to create the index, and will take longer to load the index each time searchpass.py is started, but each password checked will be incredibly fast.  Or reduce the index file to about 13 kB and make each password search through 146 MB worth of hashes.  That will be fairly slow to search for each password.
