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
        return False

    btn.click()
    WebDriverWait(driver, 8).until(lambda d: d.current_package == PKG)
    return True

def test_google_photos():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5554",
        "newCommandTimeout": 120,
        "settings[waitForIdleTimeout]": 0
    })
    driver = webdriver.Remote(APPIUM_SERVER, options=options)

    try:
        assert _open_photos_from_launcher(driver), "no photos app"

        time.sleep(1)
        candidates = [
            'new UiSelector().textContains("Search")',
        ]
        elems = []
        for q in candidates:
            elems = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, q)
            if elems:
                break
        assert elems, "no search button"
        elems[0].click()

    finally:
        driver.quit()
