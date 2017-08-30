#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from utils import *
from time import *
from log import *

class Email:
    defaultUser = "test@qq.com"
    defaultPwd = "your pwd"
    def __init__(self):
        self.user = ""
        self.pwd = ""
        self.session = None

    def emailLogin(self, user = defaultUser, pwd = defaultPwd):
        self.user = user
        self.pwd = pwd

        try:
            self.session = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
            self.session.login(user, pwd)
            WPLog("%s login success" % (user))
            return True
        except Exception, e:
            WPLog("%s emailLogin except: %s" % (user, e))
            return False

    def __del__(self):
        if self.session != None:
            self.session.quit()
            WPLog("%s logout success" % (self.user))

    def send(self, to, subject, msgText):
        msg = MIMEText(msgText)
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to

        try:
            self.session.sendmail(self.user, to, msg.as_string())
            WPLog("sendmail to %s Success" % (to))
            return True
        except Exception, e:
            WPLog("sendmail to %s except: %s" % (to, e))
            return False

def getLoginEmail():
    newEmail = Email()
    loginResult = newEmail.emailLogin()
    return loginResult, newEmail

if __name__ == '__main__':
    newEmail = Email()
    loginResult = newEmail.emailLogin()
    if loginResult == True:
        map(lambda to: newEmail.send(to, "Automatic  Hello word", "ok Hello world!"), ["test@qq.com"])
