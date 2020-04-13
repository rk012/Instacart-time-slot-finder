from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time
import sys

if sys.platform.startswith('win'):
    driver = webdriver.Chrome('.\\chromedriver.exe')
else:
    driver = webdriver.Chrome('./chromedriver')

driver.get('https://messages.google.com/web/authentication')

time.sleep(2)

remember_switch = driver.find_elements_by_xpath('/html/body/mw-app/div/main/mw-authentication-container/div/div/div/div[1]/div[1]/mat-slide-toggle/label/div/input')[0]
remember_switch.send_keys(Keys.SPACE)

print("Please log in to messages for web and select conversation to send automated sms through")

while True:
    time.sleep(0.1)
    if 'https://messages.google.com/web/conversations/' in driver.current_url:
        break

conversation_url = driver.current_url

while True:
    driver.get('https://instacart.wegmans.com/#login')

    print("Please log in to website and press ENTER once you are done adding items to your cart")
    input()

    driver.get('https://instacart.wegmans.com/store/wegmans/info?tab=delivery')
    time.sleep(2)

    if driver.current_url == 'https://instacart.wegmans.com/store/wegmans/info?tab=delivery':
        break

isNotAvailable = True

try:
    print("Scanning for available delivery time (Press CTRL+C to stop)")
    time.sleep(8)
    
    while isNotAvailable:
        try:
            delivery_element = driver.find_elements_by_xpath('/html/body/div[7]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/h1')[0]
            print("[{}] Delivery times not found".format(time.strftime("%H:%M:%S", time.localtime())))
            driver.refresh()
            time.sleep(60)
        
        except (NoSuchElementException, IndexError):
            delivery_day = driver.find_elements_by_xpath('/html/body/div[7]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div')[0]
            print("[{}] Delivery times available for {}! - ".format(time.strftime("%H:%M:%S", time.localtime()), delivery_day.get_attribute('innerHTML')))
            isNotAvailable = False
            
    driver.get(conversation_url)
    time.sleep(5)
    message_field = driver.find_elements_by_xpath('/html/body/mw-app/div/main/mw-main-container/div/mw-conversation-container/div/div/mws-message-compose/div/div[2]/div/mws-autosize-textarea/textarea')[0]
    message_field.send_keys("INSTACART BOT--Delivery time has been found for {}\n".format())
    driver.get('https://instacart.wegmans.com/store/checkout_v3')
    
except KeyboardInterrupt:
    print("KeyboardInterrupt initiated by user")

finally:
    print("Press ENTER to quit")
    input()
    print("Exiting...")
    driver.quit()
