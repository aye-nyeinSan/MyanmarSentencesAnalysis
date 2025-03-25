from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd



# ✅ Set path to chromedriver installed via Homebrew
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    # ✅ Go to the Facebook post URL
    post_url = "https://www.facebook.com/bbcnews/posts/pfbid02wvyNkAxbr66hbWQpKGZLDgsZUVR45fFM3tqpReca4DRM7KsBUz2WaVa2Vo71T3bDl"
    driver.get(post_url)
    sleep(5)  # Wait for page to load

    # ✅ Scroll to load more comments
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

    # ✅ Try expanding all "View more comments" buttons
    while True:
        try:
            more_button = driver.find_element(By.XPATH, "//div[@aria-label='View more comments']")
            driver.execute_script("arguments[0].click();", more_button)
            sleep(2)
        except:
            break

    # ✅ Get visible comment elements (adjusted XPath)
    comment_elements = driver.find_elements(By.XPATH, "//div[@role='article']//span[@dir='auto']")
    print(f"\n✅ Found {len(comment_elements)} comments\n")

    # ✅ Extract and store clean text comments
    comment_data = []
    for i, el in enumerate(comment_elements[:100], 1):
        text = el.text.strip()
        if text:
            print(f"{i}. {text}\n")
            comment_data.append({'comment_text': text})

    # ✅ Save to CSV
    df = pd.DataFrame(comment_data)
    df.to_csv("selenium_facebook_comments.csv", index=False)
    print("📁 Comments saved to selenium_facebook_comments.csv")

finally:
    driver.quit()
