import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyttsx3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


# from selenium import webdriver

# Create Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# Initialize the Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# Rest of your code...

# driver_path = "C:/users/gagan/onedrive/desktop/10x-academy/projects/controls_Browser_Using_Voice/chromedriver.exe"

# driver_path = "C:/Users/gagan/OneDrive/Desktop/10x-Academy/Projects/controls_Browser_Using_Voice/chromedriver.exe"
# service = Service(driver_path) 

# options=webdriver.ChromeOptions()

# options.binary_location=driver_path
# # driver = webdriver.Chrome(service=service, options=options)

# # options = webdriver.ChromeOptions()
# # options.binary_location = '/usr/bin/chromium-browser'
# #All the arguments added for chromium to work on selenium
# options.add_argument("--no-sandbox") #This make Chromium reachable
# options.add_argument("--no-default-browser-check") #Overrides default choices
# options.add_argument("--no-first-run")
# options.add_argument("--disable-default-apps") 
# # driver = webdriver.Chrome('/home/travis/virtualenv/python2.7.9/chromedriver',chrome_options=options)
# driver = webdriver.Chrome(service=service, options=options)
driver=webdriver.Chrome()
def wait_for_element(selector):
    return WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,selector)))

def generate_selector(button_name):
    # Generate the dynamic selector based on the button name
    return f'button[name="{button_name}"]'

def fill_input_field_by_placeholder(placeholder, data):
    input_field = wait_for_element(f'input[placeholder="{placeholder}"]')
    if input_field:
        input_field.clear()  # Clear any existing data in the input field
        input_field.send_keys(data) 

def click_element(selector):
    #  element = wait_for_element(selector)
    #  print(element)
    #  if element:
    #     # Scroll the page to bring the element into view
    #     div_element = driver.find_element(By.XPATH, '//div[@aria-label="Price"]')
    #     print(div_element)
    #     # Wait for a small delay to ensure the element is fully visible
    #     time.sleep(1)
    #     # Click the element
    #     div_element.click()
    element = wait_for_element(selector)
    if element:
        # Scroll the page to bring the element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Wait for a small delay to ensure the element is fully visible
        time.sleep(1)
        # Click the element
        action = ActionChains(driver)
        action.move_to_element(element).click().perform()

Search=''
def perform_browser_command(command):
    global Search
    if command=='open google' or command=='open Google' or command=='go to google' or command=='go to Google' or command=='visit google'or command=='visit Google':
        driver.get('https://www.google.com')

    elif command.startswith('search'):
        search_query = command[7:]
        Search=search_query
        if 'google' in driver.current_url:
    # Use locator strategy for Google search
            search_box = driver.find_element(By.NAME, 'q')
        else:
    # Use locator strategy for the input field of another site
            search_box = driver.find_element(By.ID, 'search-box-input')

        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        print("Searching for:", search_query)
    elif command == 'click on first link':
        time.sleep(2)
        xpath_expression = Search
        first_result_heading = driver.find_element(By.CSS_SELECTOR, 'a > h3')

# Extract the href attribute value of the first search result link
        # href = first_result_link.get_attribute('href')
        if first_result_heading:
            print(first_result_heading)
            first_result_heading.click()
        else:
            print("No search result links found.")
    elif command=='click on price button':
        #    button_name = command[command.rfind('on ') + 3:].rstrip('button').strip().capitalize()
        #    print(button_name)
        #    selector = f"span[aria-label='{button_name}']"
        #    print(selector)
        #    click_element(selector)
        click_element('.CustomFilter__dropdown.align-center.clickable[aria-label="Price"]')

    elif command.startswith('Set Max'):
        setQuery=command[8:]
        print(setQuery)
        fill_input_field_by_placeholder('Enter max', setQuery)
    elif command=='click on done button':
        click_element('button.button.Button.primary')

        # click_element('button.like-button')s
    elif command=='go back' or command=='visit previous page' or command=='go to previous page':
        driver.back()
    elif command=='open new tab':
        driver.execute_script('window.open("")')
    elif command=='scroll up' or command=='go down':
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    elif command=='scroll down' or command=='go up':
        driver.execute_script('window.scrollTo(0,0);')

        from selenium import webdriver

# # Launch the web browser
# driver = webdriver.Chrome()

# # Open the webpage
# driver.get("https://www.example.com")

# # Find all clickable elements on the page
# clickable_elements = driver.find_elements_by_xpath("//a | //button | //input[@type='submit']")

# # Filter the clickable elements
# filtered_elements = [element for element in clickable_elements if (element.is_enabled() and element.is_displayed())]

# # Print the extracted clickable elements
# for element in filtered_elements:
#     print(element.get_attribute("outerHTML"))

# # Close the browser
# driver.quit()


    # elif command=='click on like button':
    #     click_element('button.like-button')
    # elif command=='go back' or command=='visit previous page' or command=='go to previous page':
    #     driver.back()
    # elif command=='open new tab':
    #     driver.execute_script('window.open("")')
    # elif command=='scroll up' or command=='go down':
    #     driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    # elif command=='scroll down' or command=='go up':
    #     driver.execute_script('window.scrollTo(0,0);')
    else:
        print('Unknown command')



r=sr.Recognizer()

with sr.Microphone() as source:
    toggle=True
    while(toggle==True):
        print("...listening")

        r.adjust_for_ambient_noise(source)

        audio=r.listen(source)


        try:
            text=r.recognize_google(audio)
            print('You said:',text)
            print('toggle',toggle)
            if(text=='exit'):
                toggle=False
                driver.quit()

            perform_browser_command(text)
    
        except sr.UnknownValueError:
            print("Can not understand audio")

        except sr.RequestError as e:
            print("error in proccessing request",str(e))


        time.sleep(4)