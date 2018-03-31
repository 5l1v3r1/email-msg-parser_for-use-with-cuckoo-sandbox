# email-msg-parser_for-use-with-cuckoo-sandbox

Email Parser Code
Date Created: 03/22/2018
Author: Mark Conover
Email: mconov01@villanova.edu, conoverm157@gmail.com
Course: ECE-8489 - Malware Analysis and Defense
References (links to code that was copied/revised from):
* https://github.com/mattgwwalker/msg-extractor
    ** NOTE:  This code has an GNU General Public License (GPL), i.e. open-source license.
    ** Author:  Matthew Walker
    ** Date: 10/09/2016
    ** Version: 0.3

TODO:
    ** Install TOR node for accessing internet for malware that does network calls
    ** Install VirusTotal api key in Cuckoo Sandbox so it can connect & the "Antivirus" report tab can be filled out!
    ** Install community signatures!
    ** Install clamav signatures!
    ** Read TODO comments inside "email-parser_with-olefile-python-library-only.py"
    ** OPTIONAL (to make grade better):
        *** "email-parser_with-olefile-python-library-only.py"
            **** Unzip .zip file full of .msg files
            **** Export the email name, each attachment name to a .csv file
            **** Export .csv file and all the folders containing original emails with their attachments 
                   in their own folder so that a user can easily convert the .csv file into
                   a .xlsx (Microsoft Excel) file and can label which attachments are malicious
                   i.e. when all attachments are labeled anyone reading the csv file will
                   be able to identify the original email the malicious attachments came from
                   so they can verify those emails are removed from infected hosts and can say
                   specifically what email was the attack vector email for getting the malicious
                   attachment on the host   
        *** Cuckoo Sandbox
            **** Install Yara rules i.e. the report on email attachments is better
            **** Install volatility i.e. the report on email attachments is better

 References
 * Code Used/May Be Used to Finish Code Project:
    ** https://github.com/mattgwwalker/msg-extractor/blob/master/README.md
    ** https://github.com/mjs/imapclient
    ** https://github.com/markconover/powershell-scripts/blob/master/msg-parser_mark-conover.ps1
 * Learning Resources:
    ** https://www.lynda.com/Python-tutorials/Reading-writing-files/661773/707234-4.html
    ** https://www.safaribooksonline.com/live-training/courses/mastering-pythons-pytest/0636920158073/
    ** http://www.fileformat.info/format/outlookmsg/index.htm
    ** https://stackoverflow.com/questions/26322255/parsing-outlook-msg-files-with-python
  
 -----------------------------------------------------------------------------------------------------
 Miscellaneous Notes:
 * Start Cuckoo Manually
    ** vboxmanage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1;
    ** cuckoo -d &>> /var/log/cuckoo/CuckooService.log &
    ** cuckoo web -H 127.0.0.1 -p 9000 &>> /var/log/cuckoo/CuckooWeb.log
    ** http://127.0.0.1:9000/submit/
 * Start Umongo
    ** cd /home/mark/Documents/tools/umongo-linux-all_1-6-2
    ** ./launch-umongo.sh 
 * Cuckoo Documentation
    ** docs.cuckoosandbox.org
 * Cuckoo Installed location:
    ** /home/mark/.cuckoo/conf
 * To add a python library to Windows OS:
    1. Open command prompt.
    2. Type "pip install imapclient".
        * NOTE:  You do NOT need to also type "python".
 * VirtualBox
    ** vboxmanage showvminfo <uuid-of-vm>
------------------------------------------------------------------------------------------------------------
Cuckoo VM - Installation Notes

03/27/2018
* WireShark - Got error for unable to start capturing network traffic
    ** Solution:
        1. sudo dpkg-reconfigure wireshark-common
        2. sudo adduser -a $USER wireshark
        3. sudo chgrp wireshark /usr/bin/dumpcap
        4. sudo chmod o-rx /usr/bin/dumpcap
        5. sudo setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap
        6. sudo usermod -a -G wireshark $USER
* Copying from Windows Eclipse to Ubuntu Host
    1. sudo apt-get install dos2unix
    2. dos2unix email-parser.py
* MSG Python Library for parsing on Ubuntu (NOT Windows)
    1. sudo pip install olefile==0.43
        *** References: 
            **** http://www.decalage.info/python/olefileio#Download_and_Install
            **** http://olefile.readthedocs.io/en/latest/Howto.html
    
