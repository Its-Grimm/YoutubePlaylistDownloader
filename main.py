import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

# Main function
def main():
    browser.get("https://www.youtube.com")
    hamburgerMenu = browser.find_element(By.ID, 'guide-button')
    time.sleep(0.5)
    hamburgerMenu.click()
    
    
    
    
    
    
    # Shuts down browser tab automatically, could be usefullater
    # driver.quit()
    
if __name__ == "__main__":
    main()  