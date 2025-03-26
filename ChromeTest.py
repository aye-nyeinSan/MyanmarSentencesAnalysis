import shutil

chrome_driver = shutil.which("chromedriver")
if chrome_driver:
    print(f"✅ ChromeDriver is installed at: {chrome_driver}")
else:
    print("❌ ChromeDriver is NOT installed or not in PATH.")
