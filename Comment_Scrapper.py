from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# chrome_options.add_argument("--headless")  # Disabled for debugging

# Initialize WebDriver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

def get_comments_from_post(post_url):
    """Function to scrape comments from a single post."""
    driver.get(post_url)
    
    # Wait for the page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Comment by')]"))
    )
    
    # Allow manual scrolling
    print(f"Scroll manually through the comments for post: {post_url}")
    input("Press Enter when you're done scrolling...")

    # Wait for all comments to load after manual scrolling
    sleep(3)  # Wait for comments to finish loading after scrolling
    
    # Locate comment containers
    comment_wrappers = driver.find_elements(
        By.XPATH, "//div[contains(@aria-label, 'Comment by')]"
    )
    print(f"Found {len(comment_wrappers)} comment containers in this post")

    # Collect comment text
    comment_data = []
    for i, wrapper in enumerate(comment_wrappers, 1):
        try:
            # Extract the comment text
            comment_text_div = wrapper.find_element(
                By.XPATH, 
                ".//div[contains(@class, 'x1iorvi4') or contains(@class, 'x1lq5wgf') or contains(@class, 'x1gslohp')]//div[@dir='auto']"
            )
            text = comment_text_div.text.strip()

            if text:
                print(f"{i}. {text[:100]}..." if len(text) > 100 else f"{i}. {text}")
                comment_data.append({'comment_text': text})
            else:
                print(f"{i}. [Empty comment]")

        except Exception as e:
            print(f"Error processing comment {i}: {str(e)}")
            continue
    
    return comment_data

# List of multiple post URLs to scrape
post_urls = [
    "https://www.facebook.com/permalink.php?story_fbid=pfbid02AFD64Yk8LQou5gPcb9jd6yH4w3YWCmLNSLAUwYmqhbfgTeV67po3yMAyPCtwXuJil&id=100044432286470&__cft__[0]=AZXnSb6VWyv6iCW_IhY_h7GHu2GVjw_Hj0kgO-mYaItOOZqiy_KEyIbeHuL_ULLZhrMmpNDwddyGkUShui2OzXuGia7bjbHFyLTCUXZ3DCrwxYfGiDXs7ql9AcVFrhmB6rQeT50tDTUYZ-kGlf5AuyZCIL5sCbHYrmGs1nJh0zsmCF69bfOcN0XGnZwFWiLvSi8&__tn__=%2CO%2CP-Rg",
    "https://www.facebook.com/permalink.php?story_fbid=pfbid02LpCrJtS1SAM8hUA8sU6mc9A5jjhsLFEbHkDgxvemz24wX1EMeTz2Do4BAc8sx9Zbl&id=100044432286470&__cft__[0]=AZWCRGJ7T3Np3D3A5QptCpeNmqkgO_RakzQuQISUSMW1rVt0buuSVtoajAEHHtrii9wGvsgYSue6x4OMPeo62MurrM9LfIZZdzLvqPVctwQZ97FFulwve7YfM8Sl--semrD99v_S6n84-Ba_sB0nm4PBOgLCDBO72LgXQzAeY4pgVQ&__tn__=%2CO%2CP-R"
    # Add more post URLs here
]

# Scrape comments from all posts
all_comments = []
for post_url in post_urls:
    print(f"Processing post: {post_url}")
    comments = get_comments_from_post(post_url)
    all_comments.extend(comments)
    print(f"Finished processing post: {post_url}")

# Save comments to CSV if any are collected
if all_comments:
    df = pd.DataFrame(all_comments)
    df.to_csv("facebook_comments_clean.csv", index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} comments to facebook_comments_clean.csv")
else:
    print("No comments were collected.")

# Close the browser
driver.quit()
