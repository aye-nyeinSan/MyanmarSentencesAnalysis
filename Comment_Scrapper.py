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

def is_loading_complete(driver, prev_comment_count, timeout=5):
    """Check if comment count has stabilized"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_count = len(driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Comment by')]"))
        if current_count == prev_comment_count:
            return True
        prev_comment_count = current_count
        sleep(1)
    return False

try:
    # Go to Facebook post
    post_url = "https://www.facebook.com/permalink.php?story_fbid=pfbid02AFD64Yk8LQou5gPcb9jd6yH4w3YWCmLNSLAUwYmqhbfgTeV67po3yMAyPCtwXuJil&id=100044432286470&__cft__[0]=AZXnSb6VWyv6iCW_IhY_h7GHu2GVjw_Hj0kgO-mYaItOOZqiy_KEyIbeHuL_ULLZhrMmpNDwddyGkUShui2OzXuGia7bjbHFyLTCUXZ3DCrwxYfGiDXs7ql9AcVFrhmB6rQeT50tDTUYZ-kGlf5AuyZCIL5sCbHYrmGs1nJh0zsmCF69bfOcN0XGnZwFWiLvSi8&__tn__=%2CO%2CP-Rg"
    driver.get(post_url)
    
    # Wait for page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Comment by')]"))
    )
    
    # Improved scrolling with dynamic waiting
    last_height = driver.execute_script("return document.body.scrollHeight")
    comment_count = 0
    scroll_attempts = 0
    max_attempts = 15  # Increased from 10
    
    while scroll_attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)  # Increased from 3 seconds
        
        # Wait for comments to load
        new_comment_count = len(driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Comment by')]"))
        if new_comment_count == comment_count:
            if is_loading_complete(driver, new_comment_count):
                break
        comment_count = new_comment_count
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            sleep(3)  # Additional wait before concluding
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                
        last_height = new_height
        scroll_attempts += 1
        print(f"Scroll attempt {scroll_attempts}/{max_attempts}, Comments: {comment_count}")
    
    # Expand all "See More" buttons with more time
    see_more_buttons = driver.find_elements(By.XPATH, "//div[contains(text(), 'See more')]")
    for button in see_more_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            sleep(1.5)  # Increased from 1 second
            driver.execute_script("arguments[0].click();", button)
            sleep(2.5)  # Increased from 1 second
        except:
            continue
    
    # Expand all comments and replies with more attempts
    for _ in range(3):  # Try multiple passes
        more_btns = driver.find_elements(
            By.XPATH, 
            "//div[contains(@aria-label, 'View more comments') or contains(@aria-label, 'View more replies')]"
        )
        if not more_btns:
            break
            
        for btn in more_btns:
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                sleep(2)  # Increased from no sleep
                driver.execute_script("arguments[0].click();", btn)
                sleep(3)  # Increased from 2 seconds
            except:
                continue
        sleep(4)  # Wait between passes
    
    # Final scroll to ensure all loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    
    # Locate comment containers
    comment_wrappers = driver.find_elements(
        By.XPATH, "//div[contains(@aria-label, 'Comment by')]"
    )
    print(f"\n✅ Found {len(comment_wrappers)} comment containers\n")
    
    # Improved comment text extraction
    comment_data = []
    for i, wrapper in enumerate(comment_wrappers, 1):
        try:
            # Target the specific comment content div
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
    
    # Save to CSV
    if comment_data:
        df = pd.DataFrame(comment_data)
        df.to_csv("facebook_comments_clean.csv", index=False, encoding='utf-8-sig')
        print(f"\n📁 Saved {len(df)} comments to facebook_comments_clean.csv")
    else:
        print("\n⚠️ No valid comment text found to save.")

finally:
    input("Press Enter to close the browser...")  # Keep browser open for inspection
    driver.quit()