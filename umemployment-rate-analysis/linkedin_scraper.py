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
            
    time.sleep(2)
    driver.execute_script("document.getElementById('ember26').click();")

    # jobs_btn = driver.find_element_by_id('ember26')
    # jobs_btn.click()  

    time.sleep(2)

    paths = driver.find_elements_by_class_name('jobs-search-box__text-input')

    paths[0].send_keys("Software Developer")
    paths[2].clear()
    paths[2].send_keys("Canada")


    # jobs_search_btn = driver.find_element_by_class_name('jobs-search-box__submit-button')

    # try:
    #     jobs_search_btn.click()
    # except ElementClickInterceptedException:
    #     driver.find_element_by_class_name('msg-overlay-bubble-header').click()
    #     time.sleep(1)
    #     jobs_search_btn.click()

    # page_source = driver.page_source

    # page_soup = soup(page_source, 'html.parser')
    # # jobs = page_soup.findAll('div', {"class":"job-card-container"})
    # jobs = driver.find_elements_by_class_name('job-card-container')

    # element = driver.find_element_by_class_name("jobs-search-results") 

    # driver.execute_script( " document.querySelector('.jobs-search-results').scrollTop = 800 ")


    # for job in jobs:
    #     job.click()

    # with open("file.html", "w") as file:
    #     file.write(str(jobs))


    # jobs_desc = page_soup.findAll('div', {"class":"jobs-search-two-pane__details"})
    # with open("file2.html", "w") as file:
    #     file.write(str(jobs_desc))



    # select by value 
    # select.select_by_value('25%')


    # Enter "webdriver" text and perform "ENTER" keyboard action

    # driver.find_element(By.TAG_NAME ,"body").send_keys("hi")

    # Perform action ctrl + A (modifier CONTROL + Alphabet A) to select the page
    # driver.set_context('Chrome')

    # create action chain object 
    # action = ActionChains(driver) 
    # time.sleep(2)


    # perform the oepration 
