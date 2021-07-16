#!/usr/bin/env python3
"""
Log into aldi to see how much data I have left
"""

#standard imports
from configparser import ConfigParser
import re
import sys
from time import sleep

#3rd party imports
import humanize
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = ConfigParser()
config.read('/home/wynand/.config/passwords/aldi_mobile')
username = config["Personal_Phone"]["username"]
password = config["Personal_Phone"]["password"]
url = "https://my.aldimobile.com.au/"

ff_options = webdriver.FirefoxOptions()
ff_options.headless = True
driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver", options=ff_options, service_log_path=os.path.devnull)
driver.implicitly_wait(0.4)
driver.get(url)
driver.find_element_by_id("login_user_login").send_keys(username)
driver.find_element_by_id("login_user_password").send_keys(password)
driver.find_element_by_id("login_user_save").click()

# wait the ready state to be complete by testing if url has finished changing, but timeot after 60s
WebDriverWait(driver=driver, timeout=60).until(EC.url_changes(url))


# find the text I want
data_text = driver.find_element_by_xpath("//div[contains(@class, 'total_data')]").text
data_left = re.findall(r'\d+\.*\d*.*B$', data_text)

driver.quit()

with open("/sys/class/net/wlan0/statistics/rx_bytes", "r") as f:
    start_rx = int(f.readline())

with open("/home/wynand/.cache/lemonbar/wlan0_start", "w") as f:
    f.write(str(start_rx))

fd = sys.stdout

while True:
    with open("/home/wynand/.cache/lemonbar/wlan0_start", "r") as f:
        start_rx = int(f.readline())
    with open("/sys/class/net/wlan0/statistics/rx_bytes", "r") as f:
        now_rx = int(f.readline())
    total_rx = humanize.naturalsize(now_rx - start_rx, "%d")
    fd.write(f'D{total_rx}/{data_left[0]}')
    fd.write("\n")
    fd.flush()
    sleep(30)
