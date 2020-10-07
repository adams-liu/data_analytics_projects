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
import text_parser as tp 
import pandas as pd


def getLogin():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        username = data['email']
        password = data['password']
        return username, password

def scrape(job):
    driver.execute_script("arguments[0].click();",job)  
    time.sleep(2.5)
    job_title = driver.find_elements_by_class_name('jobs-details-top-card__job-title')[0].text
    try:
        company_name =driver.find_elements_by_class_name('jobs-details-top-card__company-url')[0].text
    except:
        company_name = "unknown"
    location = 'Canada'
    description = driver.find_elements_by_class_name('jobs-description-content__text')[0].text.lower()
    try:
        industry = driver.find_elements_by_class_name('jobs-description-details__list-item')
    except:
        industry = "unknown"
    try:
        seniority = driver.find_elements_by_class_name('jobs-box__group')[0].text
    except:
        seniority = 'unknown'
    industry_text = []
    for i in industry:
        industry_text.append(i.text)
    industry_text = industry_text[0:3]
    if 'Engineering' in industry_text:
        industry_text.remove('Engineering')
    if 'Information Technology'  in industry_text:
        industry_text.remove('Information Technology')

    level = 'Not Listed'
    seniority = seniority.splitlines()
    if seniority:
        level = seniority[1]

    technical_skills_ls = tp.getSkillsList()
    years, skills = tp.printKeywords(description,technical_skills_ls)
    return [job_title,company_name,location,str(industry_text).strip('[]'),level,years,str(skills).strip('[]')]

def toJobspage():

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

    paths[0].send_keys("Software Developer")
    paths[2].clear()
    paths[2].send_keys("Canada")

    try:
         driver.execute_script("document.getElementsByClassName('jobs-search-box__submit-button')[0].click();")
    except ElementClickInterceptedException:
        driver.execute_script("document.getElementsByClassName('msg-overlay-bubble-header')[0].click();")
        time.sleep(1)
        driver.execute_script("document.getElementsByClassName('jobs-search-box__submit-button')[0].click();")
    
    time.sleep(2)

def scrollBottom():
    driver.execute_script( "document.querySelector('.jobs-search-results').scrollTop = 1000")
    time.sleep(3)

def insertRow(df,job):
    row = scrape(job)
    row = map(lambda el:[el], row)
    temp_dict = dict(zip(columns,row))
    df2 = pd.DataFrame.from_dict(temp_dict)
    df = df.append(df2,ignore_index=True)



if __name__ == "__main__":
    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome('C:/Users/adams/Desktop/chromedriver.exe')

    toJobspage()
    scrollBottom()
    
    jobs = driver.find_elements_by_class_name('job-card-container')

    initial_list = scrape(jobs[0])
    initial_list = map(lambda el:[el], initial_list)
    columns=['job_title','company','location','industry','level','experience','skills']
    inital_dict = dict(zip(columns,initial_list))


    df = pd.DataFrame.from_dict(inital_dict)

    for i in range(1,len(jobs)):
        insertRow(df,jobs[i])



    pages = driver.find_elements_by_class_name('artdeco-pagination__indicator--number')
    for i in range(2,9):
        pages = driver.find_elements_by_xpath("//button[@aria-label='Page " + str(i) + "']")
        driver.execute_script("arguments[0].click();", pages[0]) 
        time.sleep(2)
        scrollBottom()
        jobs = driver.find_elements_by_class_name('job-card-container')
        insertRow(df,jobs[0])
        for i in range(1,len(jobs)):
            insertRow(df,jobs[i])

    df.to_csv('output.csv')


    



    