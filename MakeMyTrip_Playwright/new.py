import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def automate_makemytrip():
    # 1. Setup Chrome Options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # Attempt to bypass basic bot detection
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 2. Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # Navigate to MakeMyTrip
        print("Opening MakeMyTrip...")
        driver.get("https://www.makemytrip.com/")

        # 3. Handle the Initial Login Pop-up
        # MMT often overlays a login modal. Clicking on the page background or the close button dismisses it.
        try:
            # Wait a moment for the popup to render
            time.sleep(3)
            close_modal = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "commonModal__close")))
            close_modal.click()
            print("Closed login modal.")
        except:
            # Fallback: Click somewhere on the body to dismiss soft modals
            driver.find_element(By.CSS_SELECTOR, "body").click()

        # 4. Select "From" City
        print("Selecting Origin...")
        from_city = wait.until(EC.element_to_be_clickable((By.ID, "fromCity")))
        from_city.click()

        from_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From']")))
        from_input.send_keys("Ahmedabad")

        # Wait for the dropdown suggestion to appear and click the one matching DEL
        delhi_suggestion = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='AMD']")))
        delhi_suggestion.click()

        # 5. Select "To" City
        print("Selecting Destination...")
        to_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='To']")))
        to_input.send_keys("Bhu")

        mumbai_suggestion = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='BBI']")))
        mumbai_suggestion.click()

        # 6. Select Departure Date
        # After selecting the destination, the calendar usually drops down automatically.
        # We will select the first available future date (not disabled).
        print("Selecting Date...")
        try:
            first_available_date = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".DayPicker-Day[aria-disabled='false']")
            ))
            first_available_date.click()
        except:
            print("Could not select a date automatically.")

        # 7. Click Search
        print("Searching for flights...")
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Search')]")))
        search_btn.click()

        # 8. Wait for Results to Load
        # We wait for the specific class that wraps individual flight tickets
        flight_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listingCard")))
        print(f"Success! Found {len(flight_cards)} flight options on the page.")

        # Keep browser open briefly to observe the result
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    automate_makemytrip()