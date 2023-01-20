from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
import datetime
import traceback

from .constants import *
from .logging import logger

os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_LOCAL'] = '1'

global_browser = None


def getBrowser():
    global global_browser
    if global_browser is None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--incognito")
        if BROWSER_TYPE == 'local':
            service = ChromeDriverManager().install()
            # chrome_options.binary_location=BRAVE_BROWSER_PATH
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-gpu")
            global_browser = webdriver.Chrome(service, options=chrome_options)
        else:
            # chrome_options.platform_name = "Windows 10"
            global_browser = webdriver.Remote(SELENIUM_URL,
                                              options=chrome_options)

        global_browser.maximize_window()
        global_browser.implicitly_wait(WAIT_TIME)
    return global_browser


def clearBrowser():
    global global_browser
    global_browser = None


def navigateURL(url):
    global_browser.get(url)


def action_to_classname_controls(details, name, sleep_time):
    logger.info("action_to_classname_controls: %s " % details)
    try:
        elements = elements = global_browser.find_elements(By.CLASS_NAME, name)
        for x in range(0, len(elements)):
            try:
                if elements[x].is_displayed():
                    elements[x].click()
            except Exception as e:
                logger.info(e)
        time.sleep(sleep_time)
    except:
        logger.info("Exception in action_to_classname_controls: ", details)
        return None


def action_to_all_controls(details, name, locator, until, action, value, sleep_time):
    try:

        element_locator = get_element_locator(name, locator)
        elements = elements = global_browser.find_elements(
            element_locator, name)
        for x in range(0, len(elements)):
            try:
                action_to_element(elements[x], action, value)
            except Exception as e:
                logger.info(e)
        time.sleep(sleep_time)
    except:
        logger.info("Exception in action_to_all_controls: ", details)
        return None


def get_element_locator(name, locator):
    if locator == "ID":
        element_locator = (By.ID, name)
    elif locator == "XPATH":
        element_locator = (By.XPATH, name)
    elif locator == "CSS":
        element_locator = (By.CSS_SELECTOR, name)
    elif locator == "CLASS":
        element_locator = (By.CLASS_NAME, name)
    elif locator == "LINK":
        element_locator = (By.LINK_TEXT, name)
    elif locator == "NAME":
        element_locator = (By.NAME, name)
    elif locator == "TAG":
        element_locator = (By.TAG_NAME, name)
    elif locator == "PARTIAL_LINK":
        element_locator = (By.PARTIAL_LINK_TEXT, name)
    else:
        element_locator = None
    return element_locator


def get_element_until(until, element_locator):
    if until == "PRESENCE":
        element = WebDriverWait(global_browser, WAIT_TIME).until(
            EC.presence_of_element_located(element_locator))
    elif until == "VISIBILITY":
        element = WebDriverWait(global_browser, WAIT_TIME).until(
            EC.visibility_of_element_located(element_locator))
    elif until == "CLICKABILITY":
        element = WebDriverWait(global_browser, WAIT_TIME).until(
            EC.element_to_be_clickable(element_locator))
    elif until == "INVISIBILITY":
        element = WebDriverWait(global_browser, WAIT_TIME).until(
            EC.invisibility_of_element_located(element_locator))
    elif until == "STALE":
        element = WebDriverWait(global_browser, WAIT_TIME).until(
            EC.staleness_of(element_locator))
    else:
        element = None
    return element


def action_to_element(element, action, value):
    if action == 'click':
        element.click()
    elif action == 'send_keys':
        element.send_keys(value)
    elif action == 'clear':
        element.clear()
    elif action == 'get_attribute':
        return element.get_attribute(value)


def action_to_control(details, name, locator, until, action, value, sleep_time):
    try:
        logger.info("action_to_control: %s " % details)

        element_locator = get_element_locator(name, locator)
        if element_locator is None:
            logger.info("Invalid Locator")
            return False

        element = get_element_until(until, element_locator)
        if element is None:
            logger.info("Invalid Until")
            return False

        action_to_element(element, action, value)
        time.sleep(sleep_time)
    except Exception as e:
        logger.info("Exception in action_to_control: ", details)
        traceback.print_exc()
        return None
