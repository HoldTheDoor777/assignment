#!/usr/bin/env python
 
from imapclient import IMAPClient
import time
import RPi.GPIO as GPIO
import LCD
import SimpleMFRC522
import re

reader = SimpleMFRC522.SimpleMFRC522()
lcd = LCD.lcd()

HOSTNAME = "imap.gmail.com"
USERNAME = ""
PASSWORD = ""
MAILBOX = ""

DEBUG = True

NEWMAIL_OFFSET = 1
MAIL_CHECK_FREQ = 10


def loop():

	global USERNAME, PASSWORD, MAILBOX, HOSTNAME, lcd

	lcd.lcd_clear()
	lcd.lcd_display_string('Please tap your card',1)
        id, text = reader.read()
	if id == 142668869250:		
		USERNAME = USERNAME +  "matthewwbuckwell@gmail.com"
		PASSWORD = PASSWORD + "shatxyajdcfminry"
		MAILBOX = MAILBOX + "Inbox"
	else:
		USERNAME = "mcarcticman@hotmail.com"
		PASSWORD = "dvgboxauienynafl"
		MAILBOX = "Inbox"
	lcd.lcd_clear()
	lcd.lcd_display_string('Hello ' + text, 1)
	time.sleep(1)
	lcd.lcd_clear()
	lcd.lcd_display_string('Connecting to...',1)
	lcd.lcd_display_string(USERNAME,2)

	time.sleep(1)
	server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
        server.login(USERNAME, PASSWORD)

        if DEBUG:
                print('Logging in as ' + USERNAME)
                select_info = server.select_folder(MAILBOX)
                print('%d messages in INBOX' % select_info['EXISTS'])

        folder_status = server.folder_status(MAILBOX, 'UNSEEN')
        newmails = int(folder_status['UNSEEN'])

	messages = server.search('UNSEEN')
	newemail = server.fetch(messages, 'RFC822').items()[0][1]['RFC822']
	subject = re.search('.*Subject: (.*?)\\r\\n.*', newemail)
	lcd.lcd_display_string(subject.group(0)) 

	time.sleep(5)

	lcd.lcd_clear()
        lcd.lcd_display_string("You have " + str(newmails) +  " new email/s!",1)
	time.sleep(1)
	lcd.lcd_clear()

        time.sleep(MAIL_CHECK_FREQ)

	

if __name__ == '__main__':
        try:
                print 'Press Ctrl-C to quit.'
                while True:
                       loop()
        finally:
                GPIO.cleanup()
