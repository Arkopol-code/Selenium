from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random


def test_sourav_website(browser):  # browser comes from conftest.py
    driver = browser
    driver.get("https://souravlayek.com/")
    driver.maximize_window()

    # Run the rest of your automation steps...
    driver.find_element(By.LINK_TEXT, "Home").click()
    time.sleep(3)

    def scroll_until_found(driver, class_name, step=400, max_scroll=5000):
        """Scroll until element with given class is found or max scroll reached"""
        scrolled = 0
        while scrolled < max_scroll:
            try:
                element = driver.find_element(By.XPATH, f"//div[contains(@class, '{class_name}')]")
                driver.execute_script("arguments[0].scrollIntoView();", element)
                return element
            except NoSuchElementException:
                driver.execute_script(f"window.scrollBy(0, {step});")
                time.sleep(0.5)
                scrolled += step
        raise Exception(f"Element with class '{class_name}' not found after scrolling {max_scroll}px")

    container = scroll_until_found(driver, "flex flex-row justify-start gap-4 pl-4 max-w-7xl mx-auto")

    images = container.find_elements(By.TAG_NAME, "img")
    print(f"✅ Found {len(images)} images")

    actions = ActionChains(driver)

    for index, img in enumerate(images, start=1):
        driver.execute_script("arguments[0].scrollIntoView();", img)
        time.sleep(1)

        img.click()
        print(f"🖼 Opened image {index}")
        time.sleep(1)

        actions.send_keys(Keys.ESCAPE).perform()
        print(f"❌ Closed image {index}")
        time.sleep(1)

    driver.execute_script("window.scrollTo(0, 0);")

    driver.find_element(By.LINK_TEXT, "About Me").click()
    time.sleep(3)

    def check_link(driver, xpath):
        try:
            link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            href = link.get_attribute("href")
            print(f"🔗 Found link: {href}")

            link.click()
            time.sleep(1)

            WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            print(f"🆕 Opened new tab: {driver.current_url}")

            time.sleep(1)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(f"❌ Closed tab for {href}\n")

        except Exception as e:
            print(f"⚠ Error with link {xpath}: {e}")

    check_link(driver, "//a[contains(@href,'linkedin.com')]")
    check_link(driver, "//a[normalize-space()='Read.cv']")
    check_link(driver, "//a[normalize-space()='GitHub']")

    driver.find_element(By.LINK_TEXT, "Download Resume").click()
    windows_opened = driver.window_handles
    time.sleep(3)
    driver.switch_to.window(windows_opened[1])

    driver.close()
    driver.switch_to.window(windows_opened[0])
    driver.execute_script("window.scrollBy(0,1790);")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Let's see my works").click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
    time.sleep(2)

    time.sleep(4)

    workImages = driver.find_elements(By.XPATH, "//div[@class='row-span-1 rounded-xl group/bento max-md:!col-span-1 col-span-6 p-0 overflow-hidden']")
    for image in workImages:
        driver.execute_script("arguments[0].scrollIntoView();", image)
        image.click()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)

    driver.find_element(By.LINK_TEXT, "Blog").click()
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("Arko@gmail.com")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait = WebDriverWait(driver, 10)

    blogCards = driver.find_elements(By.CSS_SELECTOR, ".grid a")

    random_card = random.choice(blogCards)
    driver.execute_script("arguments[0].scrollIntoView(true);", random_card)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", random_card)
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    def fill_contact_form(driver, name, email, note):
        """Fill and submit the contact form"""
        driver.find_element(By.LINK_TEXT, "Contact Me").click()
        time.sleep(2)

        driver.find_element(By.ID, "name").send_keys(name)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "note").send_keys(note)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    fill_contact_form(driver, "Arko", "Arko@gmail.com", "The information is very helpful")

    time.sleep(3)
