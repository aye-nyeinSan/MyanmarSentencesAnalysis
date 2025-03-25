from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

# ✅ Optional: Headless mode (run without opening Chrome window)
chrome_options = Options()
chrome_options.add_argument("--headless=new")

# ✅ Set your ChromeDriver path (edit this path if needed)
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service,options=chrome_options)  # Add options=chrome_options if headless

try:
    # ✅ Go to Facebook post (must be logged in already)
    post_url = "https://www.facebook.com/DVBTVNews/posts/pfbid0pphvzo1kMt5v7tdBCoa6TebTwZN8chkjdVjnb2niJd4F49wft6gssbqpRk1uivMxl"
    driver.get(post_url)
    sleep(10)  # Wait for manual login or load time

    # ✅ Scroll to load more comments
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

    # ✅ Expand "View more comments" or "replies" buttons
    while True:
        try:
            more_btns = driver.find_elements(By.XPATH, "//div[@aria-label='View more comments' or @aria-label='View more replies']")
            if not more_btns:
                break
            for btn in more_btns:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    sleep(1)
                except:
                    continue
        except:
            break

    # ✅ Locate comment containers (each comment block)
    comment_wrappers = driver.find_elements(
        By.XPATH, "//div[@aria-label and contains(@aria-label, 'Comment by')]"
    )

    print(f"\n✅ Found {len(comment_wrappers)} comments and replies\n")

    # ✅ Extract only comment text (exclude name)
    comment_data = []
    for i, wrapper in enumerate(comment_wrappers, 1):
        spans = wrapper.find_elements(By.XPATH, ".//span[contains(@class, 'x1lliihq')]")
        if len(spans) >= 2:
            text = spans[1].text.strip()
            if text:
                print(f"{i}. {text}")
                comment_data.append({'comment_text': text})

    # ✅ Save to CSV
    if comment_data:
        df = pd.DataFrame(comment_data)
        df.to_csv("facebook_comments_clean.csv", index=False)
        print("\n📁 Comments saved to facebook_comments_clean.csv")
    else:
        print("⚠️ No valid comment text found to save.")

finally:
    driver.quit()
