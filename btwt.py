"""
    Daves Python/Kirbybase Reminder Program!!
    
    This program efficiently uses a timer thread to send email reminder messages to the user.
    I use this to keep track of birthdays etc without having to use any external cloud reminders.  

    The reminder data is stored in the file called events.tbl
    Also there is a built-in debug mode below, set via the debug_flag.
    
    See the readme file for db structure and further notes.
    After this is compiled into exe, I set this program to launch using windows task manager
    for every time the pc reboots.
    Enjoy!
    
    - next on list is to add ability to get data directly from GoogleSheets!
"""
import os
import sys, msvcrt
import logging
import threading
from kirbybase import KirbyBase, KBError
import datetime, math, string, time
#from	__init__ import	*
import time
from time import localtime, strftime
import smtplib
from datetime import date


# GLOBALS
myhost = 'smtp.cox.net'
datafile = 'events.tbl'

# must be set to valid email address (yours) where the email reminders will come from.
fromaddr = 'my_own_email@mygmail.com'

# set to your destination address - used for testing email in debug mode only.
toaddr = 'test@yahoo.com'

m_subject = 'By the way...'
debug_flag = 0   # set this to 1 for debug mode


# MAIL DEF
def mail(address, subject, message, host = myhost):
    headers = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s'
    message = headers % (address[0], ','.join(address[1:]), subject, message)
    try:
        server = smtplib.SMTP(host)
    except:
        logger.info("Cant connect to host for msg %s", message)
        return
    #server.set_debuglevel(1)
    server.sendmail(address[0], address[1:], message)
    server.quit()
    
# END MAIL DEF


# BROWSE_DB
def browse_db():
    now = localtime()
    mymin = strftime("%M", now)
    currday = strftime("%d", now)
    currmonth = strftime("%m", now)
    curryear = strftime("%Y", now)
    currweekday = strftime("%a", now)
   
    sendit = 0
    # Get total number of records in table.
    #if debug_flag: print 'Total records: ', db.len(datafile)
    #if debug_flag: print "\n\n"

    # COLLECT ALL RECORDS
    result = db.select('events.tbl', ['recno'], ['*'], ['eventname','eventdisp','initialdate','eventtype',
            'onetimedate','weeklyday','monthlyday','timetoremind','daysbefore','emailaddr'],
            returnType='object')

    # LOOP THRU all recs
    for rec in result:
        # save to newdisp because we will replace $calc sometimes
        newdisp = rec.eventdisp

        # DAYSBEFORE CALC
        # this only applies to ONETIME or YEARLY type of events!      
        # for 3 days before, if eventdate is 3/14/2006 then set it to 3/11/2006)
        if (rec.eventtype == "onetime") or (rec.eventtype == "yearly"):
            if (rec.eventtype == "onetime"): fdate = rec.onetimedate
            if (rec.eventtype == "yearly"): fdate = rec.initialdate
            if (rec.daysbefore > 0):
                # now need to do date subtraction by x days on the eventdate and use it later.
                difference2 = datetime.timedelta(days=-(rec.daysbefore))
                fdate = fdate + difference2

            # fill datelist array for later    
            datestr = str(fdate)
            datelist = datestr.split("-") # need this even if daysbefore is zero
            
        # WEEKLY REMINDER
	#does curr weekday = record 'weeklyday'? i.e. FRI
        if (rec.eventtype == "weekly"):
            #if debug_flag: print "\n\nIN WEEKLY"
            if (rec.weeklyday == currweekday):
                x = time.strptime(rec.timetoremind,'%H:%M')
                if strftime("%H:%M", now) == strftime("%H:%M", x):
                    sendit = 1
                    if debug_flag: print ("Will send reminder for ",rec.eventname)

        # MONTHLY REMINDER
	#does currday = records 'monthlyday'? i.e. 15
        if (rec.eventtype == "monthly"):
            if (rec.monthlyday == currday):
                x = time.strptime(rec.timetoremind,'%H:%M')
                if strftime("%H:%M", now) == strftime("%H:%M", x):
                    sendit = 1
                    if debug_flag: print ("Will send reminder for ",rec.eventname)

        # ONETIME REMINDER
        if (rec.eventtype == "onetime"):
            #if debug_flag: print "\n\nIN ONETIME"
            #if debug_flag: print "onetime event date is %s" % (rec.onetimedate)
            #if debug_flag: print 'event day is ',datelist[2]
            #if debug_flag: print "event month is ",datelist[1]
            #if debug_flag: print "time to remind is %s" % (rec.timetoremind)
            
            x = time.strptime(rec.timetoremind,'%H:%M')
            if (currday == datelist[2]) & (currmonth == datelist[1]):
                if strftime("%H:%M", now) == strftime("%H:%M", x):
                    sendit = 1
                    if debug_flag: print ("Will send reminder for ",rec.eventname)
                
        # YEARLY REMINDER  
        if (rec.eventtype == "yearly"):
            #if debug_flag: print "\n\nIN YEARLY"
            #if debug_flag: print "initial event date is %s" % (rec.initialdate)
            #print 'event day is ',datelist[2]
            #print "event month is ",datelist[1]
            #print "event year is ",datelist[0]
            x = int(curryear) - int(datelist[0]) # years since 1st one
            if (x == 1): seg = "st"
            if (x == 2): seg = "nd"
            if (x == 3): seg = "rd"
            if (x >= 4) & (x <=20): seg = "th"
            if (x > 20):
                seg = "th"
                if (str.find(str(x),"1",1,2) == 1): seg = "st"
                if (str.find(str(x),"2",1,2) == 1): seg = "nd"
                if (str.find(str(x),"3",1,2) == 1): seg = "rd"

            newdisp = str.replace(rec.eventdisp, "$calc", str(x)+seg)
            #if debug_flag: print "With message: ", newdisp
            #if debug_flag: print "time to remind is %s" % (rec.timetoremind)
            x = time.strptime(rec.timetoremind,'%H:%M')
            if (currday == datelist[2]) & (currmonth == datelist[1]):
                if strftime("%H:%M", now) == strftime("%H:%M", x):
                    sendit = 1
                    if debug_flag: print ("Will send reminder for ",rec.eventname)
                    if debug_flag: print ("With message: ", newdisp)

        # DAILY REMINDER
        if (rec.eventtype == "daily"):
            #if debug_flag: print "\n\nIN DAILY"
            x = time.strptime(rec.timetoremind,'%H:%M')
            #if debug_flag: print "DailyTIME is ",strftime("%H:%M", x)
            #if debug_flag: print "time to remind is %s" % (rec.timetoremind)
            if strftime("%H:%M", now) == strftime("%H:%M", x):
                sendit = 1
                if debug_flag: print ("Will send daily reminder for ",rec.eventname)

        if sendit:
            toaddr  = rec.emailaddr
            m_body = newdisp
            mail((fromaddr, toaddr), m_subject, m_body)
            sendit = 0
            output = "Sent %s %s" % (toaddr, m_body)
            logger.info(output)

    if debug_flag:
        print ("\n")
        print ("Current Time %s" %strftime("%H:%M", now))
        print ("Current Date is ", date.today())
        print ('Current day is ',currday)
        print ("Current month is ",currmonth)
        print ("Current year is ",curryear)
        print ("Current weekday is ",currweekday)
        print ("Next report will appear in 60 seconds...")
    return 1
# END BROWSE_DB


# HELLO
def hello():
    browse_db()

    # STOP PROGRAM
    if msvcrt.kbhit():
        if msvcrt.getch() == 'q': return

    # START NEW THREAD
    t = threading.Timer(60, hello)
    t.start() # after x seconds, hello func will be called
    
    #if t.isAlive():
    #   print ('Doctor: No.')
    #else:
    #   print ('Doctor: Next!')
# END HELLO


###############
# START MAIN  #
###############

# Uncomment one or the other of next two lines to switch between multiuser
# and embedded.  If multiuser, make sure you have a kbserver running.
db = KirbyBase()
#db = KirbyBase('client', '127.0.0.1', 44444)

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log', 'w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
print ("*")
print ("**")
print ("*** Starting...")

# verify we can connect to a mail server
print ("Testing mail server connection...")
try:
    server = smtplib.SMTP(myhost)
    print ("Mail server connection successful.")
except:
    print ("Cant connect to host for mail server: ", myhost)
    print ("Exiting program.") 
    sys.exit()
        
        
# test mail connection if in debug mode
if debug_flag:
    print ("Entering DEBUG MODE")
    print ("Sending a test email now...\n")
    headers = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s'
    message = headers % (fromaddr, toaddr, "Test email from Rex", "Body of message here.")

    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddr, message)

    print ("Exiting program since we are in DEBUG MODE.")
    server.quit()
    sys.exit()

#
# START THE INITIAL THREAD!
print ("Reminder is now up and running!")
hello()












