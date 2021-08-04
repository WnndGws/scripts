#!/usr/bin/env python3
"""
Log into aldi to see how much data I have left
"""

# standard imports
from configparser import ConfigParser
from datetime import datetime, timedelta
import os
from psutil import boot_time
import re
import subprocess
import sys
from time import sleep

# 3rd party imports
import humanize
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = ConfigParser()
config.read("/home/wynand/.config/passwords/aldi_mobile")
username = config["Personal_Phone"]["username"]
password = config["Personal_Phone"]["password"]
url = "https://my.aldimobile.com.au/"

ff_options = webdriver.FirefoxOptions()
ff_options.headless = True
driver = webdriver.Firefox(
    executable_path="/usr/bin/geckodriver",
    options=ff_options,
    service_log_path=os.path.devnull,
)
driver.implicitly_wait(0.4)
driver.get(url)
driver.find_element_by_id("login_user_login").send_keys(username)
driver.find_element_by_id("login_user_password").send_keys(password)
driver.find_element_by_id("login_user_save").click()

# wait the ready state to be complete by testing if url has finished changing, but timeot after 60s
WebDriverWait(driver=driver, timeout=60).until(EC.url_changes(url))

# find the text I want
data_text = driver.find_element_by_xpath("//div[contains(@class, 'total_data')]").text
data_left = re.findall(r"\d+\.*\d*.*B$", data_text)

driver.quit()

fd = sys.stdout
last_reboot = boot_time()
last_reboot = datetime.fromtimestamp(last_reboot).strftime("%Y-%m-%d %H:%M")


while True:
    total_rx = subprocess.run(
        ["vnstat", "--begin", str(last_reboot), "--iface", "wlan0"],
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")
    total_rx = str(total_rx.split(";")[-1]).rstrip()
    fd.write(f"D{total_rx}/{data_left[0]}")
    fd.write("\n")
    fd.flush()
    sleep(30)
