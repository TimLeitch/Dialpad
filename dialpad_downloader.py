import os
import requests
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog, Tk
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
DP_TOKEN = os.getenv('DP_TOKEN')


def init_driver():
    """Initialize and return a selenium driver."""
    return webdriver.Chrome()


def login_and_get_cookies(driver):
    """
    Log into the site and get cookies.
    :param driver: Selenium webdriver object
    :return: Dictionary of cookies
    """
    driver.get("https://dialpad.com")
    try:
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/nav/ol[2]/li[4]/div/div[1]/div/img'))
        )
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return {}
    cookies = {cookie['name']: cookie['value']
               for cookie in driver.get_cookies()}
    driver.quit()
    return cookies


def get_all(token):
    """Fetch all data and return as a Pandas DataFrame."""

    url = "https://dialpad.com/api/v2/stats"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "days_ago_end": 12,
        "days_ago_start": 1,
        "timezone": "America/Los_Angeles",
        "export_type": "records",
        "stat_type": "recordings",
    }
    try:
        response = requests.post(url, headers=headers, json=params)
    except requests.exceptions.RequestException as e:
        print(e)

    url = url + "/" + response.json()['request_id']
    response = requests.get(url, headers=headers)

    while response.json()['status'] == 'processing':
        time.sleep(1)
        response = requests.get(url, headers=headers)
    if response.json()['status'] == 'failed':
        print("Failed to get recordings")

    data = pd.read_csv(response.json()['download_url'])
    return data  # Make sure this is a DataFrame


def download_file(directory, filename, audio_url, cookies):
    """Download file and save to directory."""
    if not os.path.exists(os.path.join(directory, filename)):
        response = requests.get(audio_url, cookies=cookies)
        with open(os.path.join(directory, filename), "wb") as file:
            file.write(response.content)
            print(f"Downloaded audio file: {filename}")


def sort_by_operator(data, root_directory, cookies):
    """Sort data by operator and initiate file downloads."""
    operators = data['operator_name'].unique()  # Get unique operator names
    operators = [op for op in operators if pd.notnull(op)]  # Remove NaN values

    for operator in operators:
        directory = os.path.join(root_directory, operator.replace(
            " ", "_"))  # Replace spaces with underscores
        if not os.path.exists(directory):
            os.makedirs(directory)

    with ThreadPoolExecutor(max_workers=100) as executor:
        for _, row in data.iterrows():
            operator_name = row['operator_name']
            if pd.notnull(operator_name):
                directory = os.path.join(
                    root_directory, operator_name.replace(" ", "_"))
            else:
                name = row['name']
                if pd.notnull(name):
                    directory = os.path.join(
                        root_directory, name.replace(" ", "_"))
                else:
                    directory = os.path.join(root_directory, "unknown")

            audio_url = row['recording_url']
            filename = audio_url.split("/")[-1]+".mp3"

            executor.submit(download_file, directory,
                            filename, audio_url, cookies)
    print("Sorting complete.")


def main():
    root = Tk()
    root.withdraw()
    root_directory = filedialog.askdirectory()
    driver = init_driver()
    cookies = login_and_get_cookies(driver)
    if not cookies:
        print("Failed to obtain cookies. Exiting.")
        return
    all_data = get_all(DP_TOKEN)
    sort_by_operator(all_data, root_directory, cookies)


if __name__ == "__main__":
    main()
