from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def send_whatsapp_message(phone_number, message):
    # Set up the ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://web.whatsapp.com/")

    # Wait for user to scan the QR code
    input("Press Enter after scanning QR code")

    # Locate the search box and search for the contact
    search_box = driver.find_element(By.XPATH, '//*[@title="Search input textbox"]')
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)

    # Locate the message box and send the message
    message_box = driver.find_element(By.XPATH, '//*[@title="Type a message"]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)

    print("Message sent successfully!")

    # Close the browser after a short delay
    time.sleep(5)
    driver.quit()

# Example usage
phone_number = "+212672540196"  # Use the format with country code
message = "Hello, this is a test message from Python!"

send_whatsapp_message(phone_number, message)
