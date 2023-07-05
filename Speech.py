import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path='/chromedriver_win32.zip'

driver=webdriver.Chrome(executable_path=driver_path)

def wait_for_element(selector):
    return WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,selector)))

def click_element(selector):
    element=wait_for_element(selector)
    element.click()

def perform_browser_command(command):
    if command=='open google chrome' or command=='go to google chrome' or command=='visit google chrome':
        driver.get('https://www.google.com')
    elif command.startswith('search'):
        search_query=command[7:]

        search_box=wait_for_element('input[name="q"]')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
    elif command=='click on first link':
        click_element('div.r a')
    elif command=='click on like button':
        click_element('button.like-button')
    elif command=='go back' or command=='visit previous page' or command=='go to previous page':
        driver.back()
    elif command=='open new tab':
        driver.execute_script('window.open("")')
    elif command=='scroll up' or command=='go down':
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    elif command=='scroll down' or command=='go up':
        driver.execute_script('window.scrollTo(0,0);')
    else:
        print('Unknow command')



r=sr.Recognizer()

with sr.Microphone() as source:
    print("...listening")

    r.adjust_for_ambient_noise(source)

    audio=r.listen(source)


    try:
        text=r.recognize_google(audio)
        print('You said:',text)
    
        perform_browser_command(text)
    
    except sr.UnknownValueError:
        print("Can not understand audio")

    except sr.RequestError as e:
        print("error in proccessing request",str(e))

driver.quit()