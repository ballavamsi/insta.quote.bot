from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from helpers.logging import logger

import time
import traceback

from .constants import *
from .browser import *


def post_to_instagram(quote, filename):
    try:
        global_browser = getBrowser()
        # time.sleep(30)
        # global_browser.switch_to.window(global_browser.current_window_handle)

        time.sleep(10)
        navigateURL("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        action_to_control("accept cookie if it is displayed",
                          '//button[text()="Only allow essential cookies"]', "XPATH", "VISIBILITY", "click", "", 5)

        action_to_control("fill username", "username", "NAME",
                          "VISIBILITY", "send_keys", INSTAGRAM_USERNAME, 5)
        action_to_control("fill password", "password", "NAME",
                          "VISIBILITY", "send_keys", INSTAGRAM_PASSWORD, 5)
        # return
        action_to_control("click login button based on type submit",
                          "//*[@type='submit']", "XPATH", "VISIBILITY", "click", "", 5)
        time.sleep(10)

        if global_browser.current_url == "https://www.instagram.com/accounts/login/":
            logger.info("login failed")
            return

        global_browser.get("https://www.instagram.com/random/pagenotfound")

        action_to_control("click new post button",
                          '//*[@aria-label="New post"]', "XPATH", "CLICKABILITY", "click", "", 5)

        # select image here
        time.sleep(5)

        logger.info(filename)
        action_to_control("select image",
                          "//input[@multiple]",
                          "XPATH", "PRESENCE", "send_keys", filename, 5)

        action_to_control("click next button",
                          '//div[@role="button"][text()="Next"]',
                          # '//button[text()="Next"]',
                          "XPATH", "CLICKABILITY", "click", "", 5)

        action_to_control("click next button",
                          '//div[@role="button"][text()="Next"]',
                          # '//button[text()="Next"]',
                          "XPATH", "CLICKABILITY", "click", "", 5)

        action_to_control("send keys to textarea",
                          '//*[contains(@aria-label,"Write a caption")]',
                          "XPATH", "CLICKABILITY", "send_keys", f"{quote}\n\n{INSTAGRAM_POST}", 5)

        action_to_control("click on share button",
                          '//div[@role="button"][text()="Share"]',
                          # '//*[contains(text(),"Share")]',
                          "XPATH", "CLICKABILITY", "click", "", 5)

        action_to_control("click on svg aria-label close",
                          '//*[@aria-label="Close"]',
                          "XPATH", "CLICKABILITY", "click", "", 5)

        action_to_control("click on settings button",
                          '//*[@aria-label="Settings"]', "XPATH", "CLICKABILITY", "click", "", 5)

        action_to_control("Click on logout button",
                          '//*[contains(text(),"Log Out")]',
                          "XPATH", "PRESENCE", "click", "", 5)

        logger.info("posted to instagram")
    except Exception as e:
        traceback.print_exc()
        logger.info(e)
    finally:

        time.sleep(10)
        logger.info("Completed")
        global_browser.quit()
        clearBrowser()
