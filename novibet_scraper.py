from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from tqdm import tqdm

# URL of the page to scrape, change it to the game you want
URL = "https://www.novibet.gr/en/sports/matches/cha-hornets-tor-raptors/e37209958"

# List of query parameters used to filter different player stats categories
filters = [
    "?filter=PLAYER_POINTS",
    "?filter=PLAYER_REBOUNDS",
    "?filter=PLAYER_ASSISTS",
    "?filter=PLAYER_THREES",
    "?filter=PLAYER_DEFENSE",
    "?filter=PLAYER_COMBOS"
]
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless
chrome_options.add_argument("--disable-gpu")  # Optional: helps in some cases
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Wait to make sure the page is fully loaded
time.sleep(15)

def close_popup():
    """
    Close the introductory popup if it appears on the page.
    This function waits for the popup to become visible, then clicks
    the reject button to close it.
    """
    try:
        # Wait for the popup to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "kumulos-prompt"))
        )
        # Locate and click the "Όχι, ευχαριστώ" button to reject
        reject_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Όχι, ευχαριστώ')]")
        reject_button.click()
        print("Rejected the popup successfully.")

    except Exception as e:
        print("Popup not found or an error occurred.")

def close_reg():
    """
    Close the registration prompt if it appears on the page.
    This function waits for the registration frame to be visible,
    and then clicks the close button to dismiss it.
    """
    try:
        # Wait for the registration frame popup to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-cy='registerOrLogin']"))
        )
        print("Found the registration frame...")
        
        # Locate and click the close button on the registration frame
        close_button = driver.find_element(By.CSS_SELECTOR, "div[data-cy='closeBtn']")
        close_button.click()
        print("Closed the registration frame successfully.")
        return True

    except Exception as e:
        print("Register frame not found or an error occurred.")
        return False

# Close any popups or registration frames that might appear
close_popup()
close_reg()

# Initialize an empty list to store the scraped data
data = []

# Iterate over each filter in the filters list to gather data for each category
for filter in tqdm(filters):
    # Update the URL with the current filter and load the page
    urll = URL+filter
    driver.get(urll)
    time.sleep(10)

    # Locate all elements that contain player data using CSS selectors
    all_boxes = driver.find_elements(By.CSS_SELECTOR, "cm-card.eventMarketview.u-cmp")
    
    for box in all_boxes:
        try:
            # Extract player name and bet category from the title
            title_element = box.find_element(By.CSS_SELECTOR, "cm-card-header.u-cmp.eventMarketview_header")
            title_text = title_element.text.strip()
            
            if " - " in title_text:
                player_name, bet_category = title_text.split(" - ")
            else:
                continue  # Skip if the format isn't as expected

            # Initialize over and under values as None
            line_value = None
            over_value = None
            under_value = None

            # Locate each bet line within the box
            bet_lines = box.find_elements(By.CSS_SELECTOR, "sb-market-bet-item.marketDisplay_item.prelive")
            
            for bet_line in bet_lines:
                # Extract line type (Over/Under) and corresponding value
                line_text = bet_line.find_element(By.CSS_SELECTOR, "span.marketBetItem_caption").text.strip()
                return_value = bet_line.find_element(By.CSS_SELECTOR, "span.marketBetItem_price").text.strip()
                
                # Parse line and separate over/under values
                if "Over" in line_text:
                    line_value = line_text.replace("Over ", "").strip()  # e.g., 7.5
                    over_value = return_value
                elif "Under" in line_text:
                    line_value = line_text.replace("Under ", "").strip()  # e.g., 7.5
                    under_value = return_value

            # Append the extracted data to the list
            data.append({
                "Player Name": player_name,
                "Category": bet_category,
                "Line": line_value,
                "Over Value": over_value,
                "Under Value": under_value
            })

        except Exception as e:
            print("An error occurred:", e)
            continue
    #print("Done...")

# Convert data to DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel("Player_Bet_Data.xlsx", index=False)

driver.quit()
