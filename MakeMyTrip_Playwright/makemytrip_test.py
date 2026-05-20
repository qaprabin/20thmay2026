from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Explicit Wait Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch Chrome Browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# Open Website
driver.get("https://www.makemytrip.com")

# Maximize browser
driver.maximize_window()

# Create Explicit Wait Object
wait = WebDriverWait(driver, 10)

# Wait until body tag is visible
wait.until(
    EC.visibility_of_element_located((By.TAG_NAME, "body"))
)

print("Website opened successfully")

# Close Login Popup
driver.find_element(By.TAG_NAME, "body").click()



# Click Flights Menu
driver.find_element(
    By.XPATH,
    "//span[text()='Flights']"
).click()
