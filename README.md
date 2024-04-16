**Schedule Converter Project: Excel to iCalendar (ICS) Conversion**

This application was built for personal use, for my part-time job as an IT-assistant at Nissan NPMC

**Overview**
This project automates the process of converting your work schedule, which you download as a CSV file from Excel, into an ICS (iCalendar) file. The ICS file can then be easily imported into Google Calendar or any other calendar application that supports this format. No more manual entry of shifts!

**Features**
Input: A CSV file containing your work schedule (downloaded from Excel).

Output: An ICS file compatible with Google Calendar.

User Interaction: You’ll need to provide the name of one of the coworkers (more on this below).

**Instructions**

Download Template: Start by downloading the spreadsheet template. This template includes the necessary headers.

Fill in Your Schedule: Populate the template with your actual shift details, including the coworker names.

Export as CSV: Save your filled-in spreadsheet as a CSV file.

Startup the application using 'python manage.py runserver' in the terminal

Convert to ICS Format:
Use the website that launched to fill in the name and to upload the work schedule to export your events in iCalendar format (ICS). This format is widely supported.
The resulting ICS file will contain all your shifts.

Import into iCal (Apple Calendar):
Import the ICS file into iCal (or any other calendar app that supports ICS, I use Google Calendar).

Voilà! Your shifts are now in your calendar.

**Conclusion**
With this automated workflow, you’ll save time and avoid repetitive manual entry. Happy scheduling! 🗓️🌟
