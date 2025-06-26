
import os, json, time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

AVATAR_PATH = "avatar.jpg"

def load_cookies(driver, file_path):
    with open(file_path) as f:
        cookies = json.load(f)
    driver.get("https://facebook.com")
    for cookie in cookies:
        cookie["domain"] = ".facebook.com"
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[×] Cookie Error: {e}")
    driver.get("https://facebook.com/me")

def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(executable_path="./chromedriver", options=options)

def get_avatar():
    if os.path.exists(AVATAR_PATH):
        return AVATAR_PATH
    elif os.path.exists("avatars"):
        files = [f for f in os.listdir("avatars") if f.endswith((".jpg", ".png"))]
        if files:
            return os.path.join("avatars", random.choice(files))
    print("❌ No avatar image found.")
    exit()

def change_avatar(driver):
    driver.get("https://www.facebook.com/me")
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Edit profile picture')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//span[contains(text(),'Upload Photo')]/ancestor::div[@role='button']").click()
        time.sleep(2)
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        avatar_file = get_avatar()
        file_input.send_keys(os.path.abspath(avatar_file))
        time.sleep(4)
        driver.find_element(By.XPATH, "//div[@aria-label='Save']").click()
        print(f"✅ Avatar changed to: {avatar_file}")
    except Exception as e:
        print(f"❌ Avatar change failed: {e}")

if __name__ == "__main__":
    driver = setup_browser()
    try:
        load_cookies(driver, "fb_cookies.json")
        time.sleep(3)
        change_avatar(driver)
    finally:
        time.sleep(3)
        driver.quit()
