#!/usr/bin/env python

# Copyright (c) 2018, Mark Conover
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

__author__ = "Mark Conover"
__date__ = "2018-04-17"
__version__ = '1.0'

#
# Email (.msg files) Parser for use with Cuckoo Sandbox via Cuckoo Sandbox API.
#

import os
import sys
import olefile as OleFile
import email.utils
from email.parser import Parser as EmailParser
import traceback
import requests
import tempfile
import xlwt
from datetime import datetime

def _getStringStream(email_msg, filename, prefer='unicode'):
        """Gets a string representation of the requested filename.
        Checks for both ASCII and Unicode representations and returns
        a value if possible.  If there are both ASCII and Unicode
        versions, then the parameter /prefer/ specifies which will be
        returned.
        """

        if isinstance(filename, list):
            # Join with slashes to make it easier to append the type
            filename = "/".join(filename)

        asciiVersion = _getStream(email_msg, filename + '001E')
        unicodeVersion = windowsUnicode(_getStream(email_msg, filename + '001F'))
        if asciiVersion is None:
            return unicodeVersion
        elif unicodeVersion is None:
            return asciiVersion
        else:
            if prefer == 'unicode':
                return unicodeVersion
            else:
                return asciiVersion

def _getStream(self, filename):
    if self.exists(filename):
        stream = self.openstream(filename)
        return stream.read()
    else:
        return None
    
def windowsUnicode(string):
    if string is None:
        return None
    if sys.version_info[0] >= 3:  # Python 3
        return str(string, 'utf_16_le')
    else:  # Python 2
        return unicode(string, 'utf_16_le')













    
class email_attachment_report(object):
    def __init__(self, name, parent_msg_filename, report_url):
        self.name = name
        self.parent_msg_filename = parent_msg_filename
        self.report_url = report_url
    
def output_to_excel_file(email_attachment_report_list):
    book = xlwt.Workbook()
    sheet = book.add_sheet("CuckooReport")

    col1_name = "Email Attachment Name"
    col2_name = "Parent .msg Filename"
    col3_name = "Cuckoo Report URL"

    # Write column names
    sheet.write(0, 0, col1_name)
    sheet.write(0, 1, col2_name)
    sheet.write(0, 2, col3_name)
    
    # Write email attachment info
    row_number = 1
    for email_attachment_report in email_attachment_report_list:
        sheet.write(row_number, 0, email_attachment_report.name)
        sheet.write(row_number, 1, email_attachment_report.parent_msg_filename)
        sheet.write(row_number, 2, email_attachment_report.report_url)
        row_number += 1

    current_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    excel_output_filename = current_timestamp + "_Cuckoo-Sandbox-Analysis-Report_msg-email-attachment-files.xlsx"
    
    book.save(excel_output_filename)








if __name__ == "__main__":
    print "Starting email parser...."
    
    filename = "/home/mark/Desktop/DELETE_FILES/test-email-parser-script/Test_Email_with-email-attachments.msg"
    #filename = "C:\Users\Mark-Windows\Documents\Marks-OneDrive\OneDrive\grad-school_villanova-university\ece-8489_malware-analysis-and-defense_spring-2018\final-project\email-parser\test-emails\Test_Email_with-email-attachments.msg"
    #filename = "/Users/Mark-Windows/Documents/Marks-OneDrive/OneDrive/grad-school_villanova-university/ece-8489_malware-analysis-and-defense_spring-2018/final-project/email-parser/test-emails/Test_Email_with-email-attachments.msg"
    
    
    #email_file = olefile.open(filename, "rb")
    #email_msg = email.message_from_file(email_file)
    email_msg = OleFile.OleFileIO(filename)


    # Email Subject
    subject = _getStringStream(email_msg,'__substg1.0_0037')
    if subject is None:
        subject = "[No subject]"
    else:
        subject = "".join(i for i in subject if i not in r'\/:*?"<>|')   
    print "subject is: " + subject
    
    # Email Header
    header = ""
    try:
        header =  email_msg._header
    except Exception:
        headerText = _getStringStream(email_msg, '__substg1.0_007D')
        if headerText is not None:
            header = EmailParser().parsestr(headerText)
            #email_msg._header = EmailParser().parsestr(headerText)            
        else:
            email_msg._header = None
            header = email_msg._header
    print "header is: " + str(header)
    
            
    header_date = header['date']    
    date = email.utils.parsedate(header_date)
    dirName = '{0:02d}-{1:02d}-{2:02d}_{3:02d}{4:02d}'.format(*date)
    print "dirName for date is: " + dirName
    
    
    # Save the email attachments
    attachmentNames = []
    emailMsgAttachments = ""

    # Message - attachments()
    try:
        emailMsgAttachments = email_msg._attachments
    except Exception:
        # Get the attachments
        attachmentDirs = []

        for dir_ in email_msg.listdir():
            if dir_[0].startswith('__attach') and dir_[0] not in attachmentDirs:
                attachmentDirs.append(dir_[0])

        email_msg._attachments = []

        for attachmentDir in attachmentDirs:
            #email_msg._attachments.append(Attachment(email_msg, attachmentDir))
           
            # Get long filename
            longFilename = _getStringStream(email_msg, [attachmentDir, '__substg1.0_3707'])
            # Get short filename
            shortFilename = _getStringStream(email_msg, [attachmentDir, '__substg1.0_3704'])
            # Get attachment data
            data = _getStream(email_msg, [attachmentDir, '__substg1.0_37010102'])
            
            # Create new attachment object
            attachment_obj = type('obj', (object,), {'longFilename' : longFilename, 'shortFilename' : shortFilename, 'data' : data})
            
            # Append new attachment object
            email_msg._attachments.append(attachment_obj)

        emailMsgAttachments = email_msg._attachments
    
    # Create a file directory to contain email attachments
    #cwd = os.getcwd()
    email_attachment_temp_dir = dirpath = tempfile.mkdtemp()
    
    # Save all the email attachments to the file directory previously created
    attachmentNames = []
    absolute_filenames = []
    for emailMsgAttachment in emailMsgAttachments:    
        # Attachment - save()
        # Use long filename as first preference
        filename = emailMsgAttachment.longFilename
        # Otherwise use the short filename
        if filename is None:
            filename = emailMsgAttachment.shortFilename
        # Otherwise just make something up!
        if filename is None:
            import random
            import string
            filename = 'UnknownFilename ' + \
                ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for _ in range(5)) + ".bin"
        
        absolute_filename = os.path.join(email_attachment_temp_dir, filename)
        
        f = open(absolute_filename, 'wb')
        f.write(emailMsgAttachment.data)
        f.close()
        
        attachmentNames.append(filename)
        absolute_filenames.append(absolute_filename)
        
    # Submit each email attachment to Cuckoo Sandbox for malware analysis and
    # export Cuckoo Sandbox analysis info for all email attachments to Excel file
    email_attachment_report_list = []
    for email_attachment_name in absolute_filenames:             
        REST_URL = "http://localhost:9001/tasks/create/file"
        
    
        print "REST_URL is: " + REST_URL
        print "File sending to Cuckoo Sandbox is: " + email_attachment_name
        
        with open(email_attachment_name, "rb") as sample:
            files = {"file": (email_attachment_name, sample)}
            r = requests.post(REST_URL, files=files)
        
        task_id = r.json()["task_id"]
        report_url = "http://localhost:9001/tasks/report/" + str(task_id)
        
        print "File sent to Cuckoo Sandbox is: " + email_attachment_name + ", task_id (Cuckoo Sandbox id) is: " + str(task_id) + ", report_url is: " + report_url
        
        # Add report on email attachment to the report list
        email_attachment_report_list.append(email_attachment_report(email_attachment_name, "<NEED-TO-ADD-PARENT-MSG-FILENAME-HERE>", report_url))
    
    print "Creating Excel file with email attachment info..."
    output_to_excel_file(email_attachment_report_list)
        
                                       

