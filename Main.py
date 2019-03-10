import sys
import mechanize
import random
import datetime
import time
import math
import copy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


exp1 = '//*[@id="expedition_list"]/div[1]/div[2]/button'
exp2 = '//*[@id="expedition_list"]/div[2]/div[2]/button'
exp3 = '//*[@id="expedition_list"]/div[3]/div[2]/button'
exp4 = '//*[@id="expedition_list"]/div[4]/div[2]/button'
trainingCost = 3.0

class GladiatusBot():

    def __init__(self,email,password):
        self.browser = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.email = email
        self.password = password
        
    def signIn(self):
          
          
        try:  
            self.browser.delete_all_cookies()
            self.browser.get('https://s31-en.gladiatus.gameforge.com/game/index.php?mod=start&submod=logout&sh=eb3bd9f38532b6e2daf5c5ca0a0c6706')
            emailInput = self.browser.find_element_by_id('login_username')
            passwordInput = self.browser.find_element_by_id('login_password')
            
            emailInput.send_keys(self.email)
            passwordInput.send_keys(self.password)
            passwordInput.send_keys(Keys.ENTER)
            time.sleep(3)
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException) as error:
            print (str(error) + "Unable to login")


    def checkLoggedIn(self):
        
        try:
            
            loggedOutButton = self.browser.find_element_by_xpath('//*[@id="header_game"]/span[9]/a')
            
            if isinstance(loggedOutButton, WebElement):
                return False #if the log out button is present the person is signed in
            else:
                return True
    
    
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException) as error:
            print (str(error) + "Unable to login")
            

    def serverUpdate(self):
        
        try:
            
            refreshButton = self.browser.find_element_by_xpath('//*[@id="content_infobox"]/section/input')
            refreshButton.click()
            time.sleep(30)
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException) as error:
            print (str(error) + "No server update")    
            

    def checkExpeditionPoints(self):
    
        try:
            expeditionPoints = self.browser.find_element_by_xpath('//*[@id="expeditionpoints_value_point"]')
            if(int(expeditionPoints.text) == 0):
                self.work()
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException) as error:
            print (str(error) + "Unable to read expedition points")


            

    def expedition(self):
        
        
        try:
            
            
                self.browser.refresh()
                self.checkExpCooldown()
                
                expeditionButton = self.browser.find_elements_by_class_name('cooldown_bar_link')[0]
                expeditionButton.send_keys(Keys.ENTER)
                
                attackButton = self.browser.find_elements_by_xpath(exp3)[0] # the button to click
                attackButton.click()
                time.sleep(3)

            
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "Unable to find expedition points")
            
            
    def checkGold(self):
        
        try:
            
            
            trainingLink = self.browser.find_element_by_xpath('//*[@id="submenu1"]/a[3]')
            trainingLink.click()
            
            
            training_costs = self.browser.find_elements_by_class_name('training_costs')
            training_buttons = self.browser.find_elements_by_class_name('training_button')
            

                
            for i in range (0,len(training_costs)):
                
                gold = self.browser.find_element_by_xpath('//*[@id="sstat_gold_val"]')
                if float(training_costs[i].text) < 100 and float(training_costs[i].text) <  gold.text:
                    
                    print(training_costs[i].text)
                    training_buttons[i].click()
                    return

            
        
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "Unable to get gold count")       
            
    def checkBonus(self):
        
        try: 
            collectBonus = self.browser.find_element_by_xpath('//*[@id="linkLoginBonus"]')
            collectBonus.click()
            time.sleep(3)

        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "Bonus not ready yet")
    
    def checkLevel(self):
        
        try: 
            checkLevel = self.browser.find_element_by_xpath('//*[@id="linknotification"]')
            checkLevel.click()
            time.sleep(3)

        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "Level up not ready yet")
            
            
    def checkNotification(self):
        
        try: 
            checkNotification = self.browser.find_element_by_xpath('//*[@id="linkcancelnotification"]')
            checkNotification.click()
            time.sleep(3)
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "No notifications")


    def work(self):
        
        try: 
            workPage = self.browser.find_element_by_xpath('//*[@id="submenu1"]/a[1]')
            workPage.click()
            
            
            workMenu = self.browser.find_element_by_xpath('//*[@id="workTime"]')
            select = Select(workMenu)
            select.select_by_visible_text('8 Hours')
            
            
            
            goButton = self.browser.find_element_by_xpath('//*[@id="doWork"]')
            goButton.click()
            
            print ("No more expedition points left... sleeping for 3 hours")

            time.sleep(5400)             

            
        except (NoSuchElementException, ElementNotVisibleException, WebDriverException, IndexError) as error:
            print (str(error) + "Unable to work")           

                
    def checkExpCooldown(self):
        
        try:
            element = self.browser.find_element_by_xpath('//*[@id="cooldown_bar_text_expedition"]')

            my_time = element.text            
            myArray = my_time.split(':')
            
            print("array1: " + myArray[0] + " array2: " + myArray[1] + " array3: "+ myArray[2])
            

            hours = int(myArray[0])*3600
            minutes =int(myArray[1])*60
            seconds = int(myArray[2])
            
            print ("Sleeping for..." + str(hours + minutes + seconds))
            time.sleep(hours + minutes + seconds)
        except (NoSuchElementException, IndexError, ValueError, WebDriverException) as error:
            print (str(error) + "Expedition button not ready")

    def getQuests(self):
    
    
        try:
            
            link = self.browser.find_element_by_xpath('//*[@id="mainmenu"]/a[2]')  
            link.click()
            time.sleep(3)

        
        except (NoSuchElementException, IndexError, ValueError, WebDriverException) as error:
            print "Unable to find quest link"
            return None        
            
            
        try:
            
            elements = self.browser.find_elements_by_class_name('quest_slot_title')
        
            for element in elements:
                
                
                print element.text
                if "expeditions" in element.text:
                    
                    if "succession" not in element.text:
                        print ("TEST")
        except (NoSuchElementException, IndexError, ValueError) as error:
            print str(error) + "No quests available"          
            
            
            
            
            
#main method        
#enter your USER_NAME and PASSWORD
bot = GladiatusBot('USER_NAME', 'PASSWORD')

i = 1

bot.signIn()

while i < 1000:
    
    
    if bot.checkLoggedIn():
        print 'hello world'
        bot.signIn()
        
    bot.serverUpdate()
    bot.checkBonus()
    bot.checkLevel()
    bot.getQuests()
    bot.checkNotification()
    bot.checkGold()
    bot.checkExpeditionPoints()
    bot.checkExpCooldown()
    bot.expedition()

    i += 1
    
    
    #notes //*[@id="content"]/div[2]/div/div