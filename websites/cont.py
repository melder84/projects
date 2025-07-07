from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize web driver (make sure to replace 'path_to_web_driver_executable' with the actual path to your web driver executable)
driver = webdriver.Chrome(executable_path='path_to_web_driver_executable')

# URL of the slideshow
url = "https://example.com/slideshow"

# Open the slideshow URL
driver.get(url)

# Assuming the "Continue" button has an id attribute, replace 'continue_button_id' with the actual id of your "Continue" button
continue_button_id = "continueButton"

try:
    # Wait until the "Continue" button is clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, continue_button_id))
    )

    # Click the "Continue" button
    continue_button.click()

    print("Clicked on the 'Continue' button successfully.")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the browser window
    driver.quit()
