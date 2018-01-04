# my-own-private-reminder-program
Just a standalone reminder program written in Python to send reminder texts/emails.


Righthand Rex - My automated reminder program. 

It reminds for:
A one time event.
A daily event (same time every single day!).
A weekly event.
A monthly event.
A yearly event.
and sends a reminder TXT or EMAIL message!

DATABASE STRUCTURE:
TYPE      NAME			    EXAMPLE
string    eventname  		davids birthday
string    eventdisp		Its David's $calc Birthday Today! 
date      initialdate 		3/14/1984
string    eventtype 		(onetime, daily, weekly, monthly, yearly)
date      onetimedate		on 11/1/2005 only
string    weeklyday 		on WED each week
int       monthlyday		on the 15th of every month
string    timetoremind 		21:30
int       daysbefore		remind me x days before the actual event
string40  emailaddr		7022839723@vzwpix.com

Notes: 
Data is stored in the file called events.tbl which contains some sample reminders.
The email message body will display 'eventdisplay' using the $calc param if needed.
END
