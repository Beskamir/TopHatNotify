from selenium import webdriver
from typing import List
import time

# Struct for storing data from the config file
class ConfigData():
    websites: list=[]
    userName: str=""
    password: str=""

# Struct for combining url and the source code of that url
class WebsiteData():
    url: str = ""
    htmlSource: str = ""
    isNotifying: bool = False

# Loads the data from the config file into a struct (aka class)
def loadConfig(configFile: str) -> ConfigData:
    import configparser
    import json
    configData = ConfigData()
    iniParse = configparser.ConfigParser()
    iniParse.read(configFile)
    configData.websites = json.loads(iniParse.get("URLs","urls"))
    configData.userName = iniParse.get("Creds","userName")
    configData.password = iniParse.get("Creds","password")
    return configData

# Loads config, starts selenium server
def main(configFile: str):
    configData = loadConfig(configFile)
    while True:
        driver = getDriver()
        try:
            runSelenium(driver, configData)
        except:
            print("Caught exception!")
        driver.quit()

# Log into top hat and begin checking for differences
def runSelenium(driver, configData: ConfigData):
    print("running selenium")
    # log into tophat
    driver.get(configData.websites[0])
    time.sleep(2)  # Unknown if actually needed, but here for safety.
    # print(configData.websites[0])
    # get the username feild
    driver.find_element_by_id("username").send_keys(configData.userName)
    # print(configData.userName)
    # get the password feild
    driver.find_element_by_id("password").send_keys(configData.password)
    # print(configData.password)
    # enter/continue to next page
    driver.find_element_by_id("password").submit()
    time.sleep(4)  # Unknown if actually needed, but here for safety.


    # setup array combining urls and their html data 
    websiteArray: List[WebsiteData] = []
    for url in configData.websites:
        websiteData = WebsiteData()
        websiteData.url = url
        driver.get(url)
        time.sleep(4)  # Unknown if actually needed, but here for safety.
        websiteData.htmlSource = driver.page_source
        websiteArray.append(websiteData)

    while True:
        checkDifferences(driver, websiteArray)

# check for differences in each url's source code from what it was originally
def checkDifferences(driver, websiteArray: List[WebsiteData]):
    
    for websiteData in websiteArray:
        # print("checking Website data")
        driver.get(websiteData.url)
        time.sleep(4)  # Unknown if actually needed, but here for safety.
        # print(websiteData.url)
        # get orignal source code
        # print(websiteData.htmlSource)
        # get new source code
        if (driver.page_source != websiteData.htmlSource):
            notify(websiteData)
            websiteData.isNotifying=True
        else:
            if(websiteData.isNotifying):
                websiteData.isNotifying=False
        # compare source code with previous source code
        
        # if different the site changed (exception first run)

import os
def notify(websiteData: WebsiteData):
    if(websiteData.isNotifying):
        print("Reminder! New Top Hat question on "+websiteData.url)
        playNotifySound()
    else:
        print("Notification! New Top Hat question on "+websiteData.url)
        playNotifySound()
        if (os.name == "nt"):
            notifyWindows(websiteData.url)

from playsound import playsound
def playNotifySound():
    playsound("notifySound.wav")

from win10toast import ToastNotifier
def notifyWindows(urlName: str):
    toaster = ToastNotifier()
    toaster.show_toast("Top Hat Question!","New question on "+urlName,icon_path=None,duration=8,threaded=True)
    while toaster.notification_active(): time.sleep(0.1)
        
# get a selenium webdriver
def getDriver():
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.implicitly_wait(15)
    return driver


if __name__ == "__main__":
    main("config.ini")