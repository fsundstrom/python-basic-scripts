#!/usr/bin/python
import smtplib
fromaddr = "runakar.gotta@a.com"
toaddr = "runakar.gotta@a.com"

msg = """From: From Person <karu.gotta@a.com>
To: To Person <karur.gotta@a.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""


try:
   smtpObj = smtplib.SMTP('dc1mailrelay.ga.com')
   smtpObj.sendmail(fromaddr, toaddr, msg)
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"

