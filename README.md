# my-own-private-reminder-program
Just a standalone reminder program written in Python to send reminder texts/emails.

Righthand Rex - My automated reminder program.

It reminds for:
 - A one time event
 - A daily event (same time every single day!).
 - A weekly event.
 - A monthly event.
 - A yearly event.
 - and sends a reminder TXT or EMAIL message!

Notes: 
Data is stored in the file called events.tbl which contains some sample reminders.
The email message body will display 'eventdisplay' using the $calc param if needed.

 ### DATABASE STRUCTURE:

| TYPE | NAME | EXAMPLES |  
|-----------|:-----------:|-----------:|  
| string | eventname | David's Birthday |  
| string | eventdisp | Its David's $calc Birthday Today! |  
| date   | initialdate | 3/14/1984 |  
| string | eventtype | yearly (onetime, daily, weekly, monthly, yearly) |  
| date   | onetimedate | (for one time date reminders, otherwise ok to leave blank) |  
| string | weeklyday | WED |  
| int    | monthlyday | 15 (the 15th of every month) |  
| string | timetoremind | 21:30 |  
| int    | daysbefore | 3 (remind me 3 days before the event) |  
| string | emailaddr | test@yahoo.com |  

END
