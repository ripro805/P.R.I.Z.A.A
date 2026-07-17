import os, sys, time, tempfile, traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = os.getcwd()
PACKAGE_DIR = os.path.join(BASE_DIR, "package")
INDEX_FILE = "file:///" + os.path.join(PACKAGE_DIR, "index.html").replace(chr(92), "/")
REC_FILE = os.path.join(PACKAGE_DIR, "input.txt")
LOG_FILE = os.path.join(PACKAGE_DIR, "speech_log.txt")

print("[BOOT] CWD =", BASE_DIR)
print("[BOOT] Saving transcripts to:", REC_FILE)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
profile_dir = os.path.join(tempfile.gettempdir(), "prizaa_chrome_" + str(int(time.time())))
chrome_options.add_argument("--user-data-dir=" + profile_dir)

service = Service(ChromeDriverManager().install())
service.start()
driver = None

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(900, 700)
    driver.get(INDEX_FILE)

    start_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "start-button"))
    )
    start_button.click()
    print("[READY] Mic capture started. Press Ctrl+C to stop.")

    last_text = ""
    while True:
        try:
            output_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "output"))
            )
            current_text = output_element.text.strip()
        except Exception:
            current_text = last_text

        if current_text and current_text != last_text:
            last_text = current_text
            line = "USER: " + current_text
            print(line)
            with open(REC_FILE, "w", encoding="utf-8") as f:
                f.write(line + "\n")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("[STOP] Interrupted by user.")
except Exception as e:
    print("[ERROR]", e)
    traceback.print_exc()
finally:
    try:
        if driver is not None:
            driver.quit()
    except Exception:
        pass
    try:
        service.stop()
    except Exception:
        pass
    try:
        import shutil
        shutil.rmtree(profile_dir, ignore_errors=True)
    except Exception:
        pass