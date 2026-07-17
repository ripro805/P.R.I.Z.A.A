import os
import sys
import time
import tempfile
import shutil
from os import getcwd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

profile_dir = os.path.join(tempfile.gettempdir(), "prizaa_chrome_" + str(int(time.time())))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
chrome_options.add_argument("--user-data-dir=" + profile_dir)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

service = Service(ChromeDriverManager().install())
service.log_path = os.path.join(getcwd(), "chromedriver.log")
service.start()

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    website = "file:///" + getcwd().replace(chr(92), "/") + "/package/index.html"
    driver.get(website)

    rec_file = getcwd() + chr(92) + "package" + chr(92) + "input.txt"
    log_file = getcwd() + chr(92) + "package" + chr(92) + "speech_log.txt"

    def listen():
        start_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "start-button"))
        )
        start_button.click()
        print("[READY] Microphone is live. Speak now...", flush=True)
        print("[SAVE]  " + rec_file, flush=True)
        print("-" * 60, flush=True)
        output_text = ""
        while True:
            try:
                output_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "output"))
                )
                current_text = output_element.text.strip()
                if current_text and current_text != output_text:
                    output_text = current_text
                    line = "USER: " + " ".join(output_text.lower().split())
                    print(line, flush=True)
                    with open(rec_file, "w", encoding="utf-8") as f:
                        f.write(line + chr(10))
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(line + chr(10))
            except Exception as inner:
                msg = str(inner)
                if "no such window" in msg or "tab crashed" in msg:
                    raise
                continue

    try:
        listen()
    except KeyboardInterrupt:
        print(chr(10) + "[STOP] Interrupted by user.", flush=True)
    except Exception as e:
        print("Error occurred: " + str(e), flush=True)
finally:
    try:
        driver.quit()
    except Exception:
        pass
    try:
        service.stop()
    except Exception:
        pass
    try:
        shutil.rmtree(profile_dir, ignore_errors=True)
    except Exception:
        pass

