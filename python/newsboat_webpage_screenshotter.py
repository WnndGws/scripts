#!/usr/bin/env python3
"""Take a tall screenshot of a page so i dont have to open my browser since I'm lazy."""
import os
from time import sleep

import click
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


@click.command()
@click.option("--url")
@click.option("--seconds", default=5)
def get_screenshot(url: str, seconds: int):
    """Take a tall screenshot into temp dir."""
    # Set up webdriver
    binary = FirefoxBinary("/bin/firefox")

    ff_options = webdriver.FirefoxOptions()
    ff_options.headless = True
    driver = webdriver.Firefox(
        firefox_binary=binary,
        executable_path="/bin/geckodriver",
        options=ff_options,
        service_log_path=os.path.devnull,  # Dont log
    )
    driver.get(url)

    # the element with longest height on page
    driver.set_window_size(1920, seconds * 1500)  # just hardcode tall since im lazy
    sleep(seconds)  # Time for page to load
    driver.get_screenshot_as_file("/tmp/browser.png")
    driver.quit()


if __name__ == "__main__":
    get_screenshot()
