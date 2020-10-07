import time
import bs4 #beautifulsoup
import yaml
from selenium import webdriver # import web driver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.select import Select
# import Action chains  
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
import parser_test as tp 


def getLogin():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        username = data['email']
        password = data['password']
        return username, password
    

if __name__ == "__main__":
    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome('C:/Users/adams/Desktop/chromedriver.exe')
    driver.maximize_window()

    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.25);')


    driver.get('https://www.linkedin.com/uas/login')

    username , password = getLogin()
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)


    driver.execute_script("document.getElementsByClassName('btn__primary--large')[0].click();")
            
    time.sleep(1)
    driver.execute_script("document.getElementById('ember26').click();")

    time.sleep(2)

    paths = driver.find_elements_by_class_name('jobs-search-box__text-input')

    paths[0].send_keys("New Grad: Waveserver")
    paths[2].send_keys("Canada")

    try:
         driver.execute_script("document.getElementsByClassName('jobs-search-box__submit-button')[0].click();")
    except ElementClickInterceptedException:
        driver.execute_script("document.getElementsByClassName('msg-overlay-bubble-header')[0].click();")
        time.sleep(1)
        driver.execute_script("document.getElementsByClassName('jobs-search-box__submit-button')[0].click();")
  


    time.sleep(2)
    driver.execute_script( "document.querySelector('.jobs-search-results').scrollTop = 1000")
    time.sleep(2)
    jobs = driver.find_elements_by_class_name('job-card-container')

    

    job_title = driver.find_elements_by_class_name('jobs-details-top-card__job-title')[0].text
    company_name =driver.find_elements_by_class_name('jobs-details-top-card__company-url')[0].text
    location = driver.find_elements_by_class_name('jobs-details-top-card__bullet')[0].text
    description = driver.find_elements_by_class_name('jobs-description-content__text')[0].text.lower()
    industry = driver.find_elements_by_class_name('jobs-description-details__list-item')
    seniority = driver.find_elements_by_class_name('jobs-description-details')[0].text
    industry_text = []
    for i in industry:
        industry_text.append(i.text)

    level = 'Not Listed'
    seniority = seniority.splitlines()
    for i in range(len(seniority)):
        if i == "Seniority Level":
            level = seniority[i+1]
    
    technical_skills_ls = tp.getSkillsList()
    years, skills = tp.printKeywords(description,technical_skills_ls)
    print(job_title,company_name,location,industry_text[0:3],level,years,skills)
