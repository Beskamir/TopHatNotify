# Top Hat Notify
Simple Python script to notify me when a new Top Hat question is posted. 

Now you can safely skip class and still be notified when the prof posts a Top Hat question!

---
## Features
 - Works with multiple Top Hat courses
 - Plays notification sound (notifySound.wav)
 - Prints notification to console
 - On Windows, sends a proper Windows notification
---
## Setup and Install

### Setup your config.ini file
 - Rename sampleConfig.ini to config.ini 
 - Fill it with
   - Your credentials
   - The Top Hat urls you want it to check

### Install the necessary libraries (some of these should be installed by default but I'll list them anyway)
    pip install selenium
    pip install playsound
    pip install win10toast
    pip install typing
    pip install time
    pip install configparser
    pip install json
    pip install os

### Run the Python file
    py -3 .\Notify.py
---
## Platform/Python Requirments
 - Developed and tested on Windows 10
 - Should be crossplatform except for win10toast
 - Uses Python 3 but it might be compatible with Python 2

## Known issues
 - Might have some false positives

## Nice to have features that I probably won't implement unless I get bored
 - Different notification sound for first message vs reminders
 - Time stamp the notifications when printing them to the console