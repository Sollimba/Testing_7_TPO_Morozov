import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

APPIUM_SERVER = "http://127.0.0.1:4723"
PKG = "com.google.android.apps.photos"

def _open_photos_from_launcher(driver):
    btn = None
    for sel in (
        ('textContains', 'Photos'),
    ):
        try:
            by = f'new UiSelector().{sel[0]}("{sel[1]}")'
            btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, by)
            break
        except Exception:
            continue

    if not btn:
        print("ERROR: Google Photos not found on launcher")
        return False

    btn.click()
    try:
        WebDriverWait(driver, 8).until(lambda d: d.current_package == PKG)
    except Exception:
        print("ERROR: Google Photos did not open in 8 seconds")
        return False
    return True

def test_google_photos():
    # Опции подключения
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5554",  # ID эмулятора из adb devices
        "newCommandTimeout": 120,
        "settings[waitForIdleTimeout]": 0
    })

    print("Connecting to Appium server...")
    driver = webdriver.Remote(APPIUM_SERVER, options=options)

    # Вывод капабилити для отладки
    print("Device capabilities check")
    print("Device name:", driver.capabilities.get("deviceName"))
    print("Platform:", driver.capabilities.get("platformName"))
    print("Current package:", driver.current_package)

    try:
        if not _open_photos_from_launcher(driver):
            print("TEST FAILED: cannot open Google Photos")
            return

        print("Google Photos opened. Searching for 'Search' button...")
        time.sleep(1)
        candidates = [
            'new UiSelector().textContains("Search")',
        ]
        elems = []
        for q in candidates:
            elems = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, q)
            if elems:
                break

        if not elems:
            print("TEST FAILED: 'Search' button not found")
        else:
            print("'Search' button found. Clicking...")
            elems[0].click()
            print("TEST PASSED: Search button clicked")

    finally:
        driver.quit()
        print("Driver session ended")

if __name__ == "__main__":
    test_google_photos()