from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.request import urlretrieve  
from datetime import datetime
from random import seed
from random import randint
from .models import *
import time
import os
import re 

import pandas
seed(1)

from django.shortcuts import render
isOccupied = False


def index(request):
    

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    PATH = os.path.realpath('input.xlsx')
    excel_data_df = pandas.read_excel(PATH , sheet_name='Sheet1')

    START_INDEX_FOR_URL = int(excel_data_df['Start_url_index'].tolist()[0])
    END_INDEX_FOR_URL = (excel_data_df['End_url_index'].tolist()[0])


    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--remote-debugging-port=9222")
    chromeOptions.add_argument('--no-sandbox')


    driver = webdriver.Chrome(os.path.abspath('chromedriver.exe'),options=options)



    username= 'Profile-Maker'
    password= 123456
    def createURL(currentURLNUMBER):
            url = 'https://www.lustvolledates.de/profile/{}/preview'.format(currentURLNUMBER)
            return url
        

    # ################################################################################
    # ##########################  Saving image  Part  ##############################
    # ################################################################################
    def getGender():
        try:
            gender = driver.find_element_by_xpath('//*[@id="left-sidebar"]/div[5]/div[2]/p[1]').get_attribute('innerHTML')
            result = gender.find('Weiblich')
            if result != -1:
                return True
            else:
                return False
        except:
            return False


    import wget
    import requests
    import shutil

    def getImage():

        url = driver.find_element_by_xpath('//*[@id="left-sidebar"]/a/img').get_attribute('src')
        print(url)
        if url == 'https://www.lustvolledates.de/storage/profile_images/a/a/a/aaaa.jpg':
            print('profile not found ! operation suspended')
            raise Exception

        filename = 'test.jpg'

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
            print('Image sucessfully Downloaded: ',filename)
            return True
        else:
            print('Image Couldn\'t be retreived')
            return False


    def getExtractedEYECOLOR(string):
        start_index=string.index('Augenfarbe:')
        end_index= start_index+ len('Augenfarbe:')
        return string[end_index:].strip()


    def getExtractedHAIRCOLOR(string):
        start_index=string.index('Haarfarbe:')
        end_index= start_index+ len('Haarfarbe:')
        return string[end_index:].strip()


    def getEyeColor():
        try:
            return getExtractedEYECOLOR(driver.find_element_by_xpath('//*[@id="left-sidebar"]/div[5]/div[2]/p[16]').get_attribute('innerHTML'))
        except:
            print('no eye color found')
            return 'Bitte auswählen'

    def getHairColor():
        try:
            return getExtractedHAIRCOLOR(driver.find_element_by_xpath('//*[@id="left-sidebar"]/div[5]/div[2]/p[17]').get_attribute('innerHTML'))
        except:
            print('no eye hari found')
            return 'Bitte auswählen'


    # ################################################################################
    # ##########################  Description Part  ##############################
    # ################################################################################

    def getProfileTextDescription():
        return driver.find_element_by_xpath('//*[@id="left-sidebar"]/div[4]/div[2]').get_attribute('innerHTML')

    def getProfileUsername():
        username = driver.find_element_by_xpath('//*[@id="left-sidebar"]/h1').get_attribute('innerHTML')
        return username

    def getProfileUsernameStriped():
        username = driver.find_element_by_xpath('//*[@id="left-sidebar"]/h1').get_attribute('innerHTML')
        start_index = username.index('(')
        username=username[:start_index].strip()
        return username



    # ################################################################################
    # ##########################  Age Calculation Part  ##############################
    # ################################################################################

    def getAgeExtracter(string):
        start_index = string.index('(')+1
        end_index = string.index(')')
        string = string.replace(' ','')
        return int(string[start_index:end_index].strip())

    def getMonth():
        month = randint(10, 12)
        if month ==2:
            return 3
        else:
            return month

    def getDay():
        day = randint(10, 30)
        return day
        
    def makeDate(ans):
            return '{}/{}/{} '.format(getMonth(),getDay(),ans)

    def getProfileAge(string):
        age= getAgeExtracter(string)
        now = datetime.now()
        ans = now.year - age
        return makeDate(ans)

    def getRandomNumber():
        month = randint(1, 12)
        return month

        


    # ################################################################################
    # ##########################     Main Function        ###########################
    # ################################################################################
    # https://www.lustvolledates.de/storage/profile_images/a/a/a/aaaa.jpg
    def checkAlert():
            driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]').click()

    def checkDescription(string):
        regex = '/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/'
        match = re.findall(r'[\w\.-]+@[\w\.-]+', string)

        ##############################################################
        ########################## Email Portion #####################
        ##############################################################

        if len(match) == 0:
            return True
        else:
            return False
        ##############################################################
        ########################## url links Portion #####################
        ##############################################################        
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)
        if len(urls) == 0:
            return True
        else:
            return False

        ##############################################################
        ########################## url links Portion #####################
        ##############################################################        
        social_media_link1 = re.findall('instagram', string)
        social_media_link2 = re.findall('facebook', string)
        social_media_link3 = re.findall('Twitter', string)
        social_media_link4 = re.findall('facebook', string)
        social_media_link5 = re.findall('snapchat', string)
        social_media_link6 = re.findall('telegram', string)
        if len(social_media_link1) == 0 and len(social_media_link2) == 0 and len(social_media_link3) == 0 and len(social_media_link4) == 0 and len(social_media_link5) == 0 and len(social_media_link6) == 0:
            return True
        else:
            return False
        
        # 
        ##############################################################
        ########################## Phone Number #####################
        ############################################################## 
        phones = re.findall(r'(?<!\d)[0-9]{4}', string)
        if len(phones) == 0:
            return True
        else:
            return False

    def getURLS(currentURLNUMBER):
        driver.get(createURL(currentURLNUMBER))
        sleep(3)
        try:
            checkAlert()
        except:
            pass

        driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/button').click()

        try:
            profileUsername = getProfileUsername()
        except:
            print('no username found .... dismental operation')
            return 
        try:
            image = getImage()
        except:
            print('no image found .... dismental operation')
            return

        if not checkDescription(getProfileTextDescription()):
            print('description is not acceptable .... dismental operation')
            return


        if getGender():
            image = getImage()
            eyeColor = getEyeColor()
            hairColor = getHairColor()
            profileDesc = getProfileTextDescription()
            profileUsername = getProfileUsername()
            profileAge = getProfileAge(profileUsername)
            profileUsername = getProfileUsernameStriped()
            lst = {}
            lst['eyeColor'] = eyeColor
            lst['hairColor'] = hairColor
            lst['profileAge'] = profileAge
            lst['profileUsername'] = profileUsername
            lst['profileDesc'] = profileDesc
            
            return lst


    # ################################################################################
    # #######               Profile  Function after scrapping the data             ###
    # ################################################################################

    def loginForProfileCreation():
        driver.get('http://meinadmin.center/old/create_v2?&slot=1110')
        driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        
    def checkUsername(name):
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="checkUsername"]').click()
        sleep(3)

        if  driver.find_element_by_xpath('//*[@id="checkUsername_result"]').get_attribute('innerHTML') == 'Benutzername ist frei':
            global isOccupied
            isOccupied=True
            return name
        else :
            raise Exception
            # driver.find_element_by_xpath('//*[@id="username"]').clear()
            # return checkUsername( name+str(getRandomNumber()) )
        

    def passDateOfBirth(dob):
        driver.find_element_by_xpath('//*[@id="age"]').send_keys(dob)
        print('date of birth passed')

    def passProfilePicture():
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/form/div[2]/div[2]/div/div[2]/p[1]/input').send_keys(os.path.realpath('test.jpg'))
        print('profile picture passed')

    def passProfileDesction(desc):
        driver.find_element_by_xpath('//*[@id="desc"]').send_keys(desc)
        print('profile description passed')

    def passLookingForWomen():
        driver.find_element_by_xpath('//*[@id="lookingfor_radio_Frau"]').click()
        print('profile looking for woman passed')

    def passGreetingText():
        lst = [6,16,26,36,46]
        select = Select(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/form/div[2]/div[1]/div/div[2]/div[2]/div[3]/select'))
        selectIndex = randint(0, 4)
        select.select_by_value(str(lst[selectIndex]))
        print('passed random greetings')

    def passSearchForWomen():
        select = Select(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/form/div[2]/div[1]/div/div[2]/div[2]/div[1]/select'))
        select.select_by_value('1')
        print('passed what u want man')


    def makeEyeID(string):
        return '//*[@id="eye_radio_{}"]'.format(string)

    def makeHairID(string):
        return '//*[@id="hair_radio_{}"]'.format(string)
        # //*[@id="hair_radio_Blond"]
        # //*[@id="hair_radio_Weiß"]

    def passEyeColor(string):
        driver.find_element_by_xpath(makeEyeID(string)).click()
        print('eye color passed')

    def passHairColor(string):
        driver.find_element_by_xpath(makeHairID(string)).click()
        print('hair color passed')


    def selectFixInputs():

        # click for job
        driver.find_element_by_xpath('//*[@id="job_radio_Bitte auswählen"]').click()
        # click for smoking
        driver.find_element_by_xpath('//*[@id="smoking_radio_Bitte auswählen"]').click()
        # click on drinking 
        driver.find_element_by_xpath('//*[@id="drinking_radio_Bitte auswählen"]').click()
        # click on relationship
        driver.find_element_by_xpath('//*[@id="relationship_radio_Bitte auswählen"]').click()
        # click on lastrelationship
        driver.find_element_by_xpath('//*[@id="lastrelationship_radio_Bitte auswählen"]').click()
        # click on living
        driver.find_element_by_xpath('//*[@id="living_radio_Bitte auswählen"]').click()
        # click on body type
        driver.find_element_by_xpath('//*[@id="body_radio_Normal"]').click()
        print('fixed input passed')


    def passProfileDetail(eyeColor , hairColor , profileAge , profileUsername , profileDesc, currentURLNUMBER):
        try:
            loginForProfileCreation()
        except:
            print('no login requirred')
            pass

        try:
            checkUsername(profileUsername)
            driver.find_element_by_xpath('//*[@id="username"]').clear()

        except:
            print('username occupied')
            return
        newUsername = checkUsername(profileUsername)
        passDateOfBirth(profileAge)
        passProfilePicture()
        passProfileDesction(profileDesc)
        passLookingForWomen()
        passGreetingText()
        passSearchForWomen()
        selectFixInputs()
        passEyeColor(eyeColor)
        passHairColor(hairColor)
        sleep(5)

        driver.find_element_by_xpath('//*[@id="height_int_"]').clear()
        driver.find_element_by_xpath('//*[@id="height_int_"]').send_keys(0)
        driver.find_element_by_xpath('//*[@id="plz"]').clear()
        driver.find_element_by_xpath('//*[@id="plz"]').send_keys(99999 )
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/form/div[3]/div[2]/div/button').click()

        
        sleep(5)

        print('Profile Completely Copied Successfully ' + str(currentURLNUMBER) )


    for i in range(START_INDEX_FOR_URL,END_INDEX_FOR_URL ):
        # try:
            lst= getURLS(START_INDEX_FOR_URL) 
            START_INDEX_FOR_URL+=10
            passProfileDetail(
                eyeColor = lst['eyeColor'] ,
                hairColor = lst['hairColor'] ,
                profileAge = lst['profileAge'] ,
                profileUsername = lst['profileUsername'],
                profileDesc = lst['profileDesc'] ,
                currentURLNUMBER=START_INDEX_FOR_URL
                )
            global isOccupied 
            Profiles.objects.create(
                profileNo=START_INDEX_FOR_URL,
                eyeColor = lst['eyeColor'] ,
                haircolor = lst['hairColor'] ,
                profileAge = lst['profileAge'] ,
                profileUsername = lst['profileUsername'],
                profileDesc = lst['profileDesc'] ,
                isOccupied = isOccupied
                )
            print(START_INDEX_FOR_URL)

            excel_data_df['Start_url_index'].iloc[0] = START_INDEX_FOR_URL
            excel_data_df.to_excel('input.xlsx',index=False) 
            
        # except:
        #     currentURLNUMBER+=10
        
        



