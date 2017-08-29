#coding:utf-8
import smtplib
import imaplib
from email.mime.text import MIMEText
from utils import *
from time import *

class Email:
    defaultUser = "test@qq.com"
    defaultPwd = "your pwd"
    def __init__(self):
        self.user = ""
        self.pwd = ""
        self.session = None

    def smtpLogin(self, user = defaultUser, pwd = defaultPwd):
        self.user = user
        self.pwd = pwd

        try:
            self.session = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
            self.session.login(user, pwd)
            print "%s: %s login success" % (getTimeStr(), user)
            return True
        except Exception, e:
            print "%s: %s emailLogin except: %s" % (getTimeStr(), user, e)
            return False

    def __del__(self):
        if self.session != None:
            self.session.quit()
            print "%s: %s logout success" % (getTimeStr(), self.user)

    def send(self, to, subject, msgText):
        msg = MIMEText(msgText)
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to

        try:
            self.session.sendmail(self.user, to, msg.as_string())
            print "%s: sendmail to %s Success" % (getTimeStr(), to)
            return True
        except Exception, e:
            print "%s: sendmail to %s except: %s" % (getTimeStr(), to, e)
            return False

def getLoginEmail():
    newEmail = Email()
    loginResult = newEmail.emailLogin()
    return loginResult, newEmail

import re

def imap4(host, port, usr, pwd, use_ssl):
    """Imap4 handler

    :param host: host
    :param port: port
    :param usr: username
    :param pwd: password
    :param use_ssl: True if use SSL else False
    """
    # Connect to mail server
    try:
        conn = imaplib.IMAP4_SSL("imap.qq.com", 993)
        conn.login("linzistudio@qq.com", "kenegrtwbpwbjehg")
        print("[+] Connect successfully")
    except BaseException as e:
        print ("Connect to {0}:{1} failed".format(host, port), e)
        return

    # Initial some variable
    list_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    download_num = 0
    download_hash = []

    # Get all folders
    try:
        type_, folders = conn.list()
    except BaseException as e:
        print ("Get folder list failed", e)
        return

    for folder in folders:
        # Parse folder info and get folder name
        try:
            flags, delimiter, folder_name = list_pattern.match(folder).groups()
            folder_name = folder_name.strip('"')
            print "[*] Handling folder: {0}".format(folder_name)
        except BaseException as e:
            print "[-] Parse folder {0} failed: {1}".format(folder, e)
            continue

        # Select and search folder
        try:
            conn.select(folder_name, readonly=True)
            type_, data = conn.search(None, "ALL")
        except BaseException as e:
            print "[-] Search folder {0} failed: {1}".format(folder_name, e)
            continue

        # Get email number of this folder
        try:
            msg_id_list = [int(i) for i in data[0].split()]
            msg_num = len(msg_id_list)
            print "[*] {0} emails found in {1} ({2})".format(msg_num, usr, folder_name)
        except BaseException as e:
            print "[-] Can't get email number of {0}: {1}".format(folder_name, e)
            continue

        # Get email content and attachments
        for i in msg_id_list:
            print "[*] Downloading email {0}/{1}".format(i, msg_num)

            # Get email message
            try:
                type_, data = conn.fetch(i, "(RFC822)")
                msg = email.message_from_string(data[0][1])
            except BaseException as e:
                print "[-] Retrieve email {0} failed: {1}".format(i, e)
                continue

            # If message already exist, skip this message
            try:
                msg_md5 = md5(data[0][1]).hexdigest()
                if msg_md5 in download_hash:
                    print "[-] This email has been downloaded in other folder"
                    continue
                else:
                    download_hash.append(msg_md5)
                    download_num += 1
            except BaseException as e:
                print "[-] Parse message md5 failed: {0}".format(e)
                continue

            # Parse and save email content/attachments
            try:
                pass#parse_email(msg, download_num)
            except BaseException as e:
                print "[-] Parse email {0} failed: {1}".format(i, e)

    # Logout this account
    conn.logout()
if __name__ == '__main__':
    imap4("linzistudio@qq.com", 993, "linzistudio@qq.com", "kenegrtwbpwbjehg", 1)
    '''
    try:
        conn = imaplib.IMAP4_SSL("imap.qq.com", 993)
        conn.login("linzistudio@qq.com", "kenegrtwbpwbjehg")
        print("[+] Connect successfully")

        conn.logout()
    except Exception, e:
        exit_script("Connect to failed", e)


    newEmail = Email()
    loginResult = newEmail.smtpLogin()
    if loginResult == True:
        map(lambda to: newEmail.send(to, "Automatic  Hello word", "ok Hello world!"), ["linzistudio@qq.com"])
    '''