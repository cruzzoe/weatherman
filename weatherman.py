import datetime
import os
import subprocess
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

load_dotenv()

TOKEN = os.getenv("TOKEN")
HOME_IP = os.getenv("HOME_IP")


def notify(header, message):
    cmd = f'curl "http://{HOME_IP}:8991/message?token={TOKEN}" -F "title=[{header}]" -F "message"="{message}" -F "priority=5"'
    subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


def determine_weather():
    """Use selenium to determine the weather in Tokyo and notify"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(
        "https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=1310300&lang=en"
    )
    driver.implicitly_wait(0.5)

    time.sleep(2)
    # Get the HTML content of the page
    html = driver.page_source
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find_all("img", class_="forecast-icon")[0]
    description = tag.get("title")
    max_temp_elements = soup.find_all("td", class_="forecast-max-temp")
    min_temp_elements = soup.find_all("td", class_="forecast-min-temp")
    min_t = min_temp_elements[0].get_text(strip=True)
    max_t = max_temp_elements[0].get_text(strip=True)
    today = datetime.datetime.today()
    today = today.strftime("%A")
    notify(f"Weather: {today}", f"{description} Min {min_t}, Max {max_t}")
    driver.quit()


if __name__ == "__main__":
    determine_weather()
