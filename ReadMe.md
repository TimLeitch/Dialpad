# Dialpad Downloader

This script allows you to download audio files from the Dialpad website and organize them by operator.

## Prerequisites

- Python 3.x
- Chrome web browser

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages by running the following command:
    ```
    pip install -r requirements.txt
    ```
3. Make sure you have Chrome browser installed on your machine.

## Usage

1. Set the `DP_TOKEN` environment variable with your Dialpad API token.
   Or create a `.env` file in the same directory as the script with the following content:
      ```
      DP_TOKEN=your_api_token
      ``` 
2. Run the script by executing the following command:
    ```
    python dialpad_downloader.py
    ```
3. A file dialog will appear. Select the directory where you want to save the downloaded audio files.
4. The script will open the Dialpad website.
5. Log in to your Dialpad account either with username and password or SSO. 
6. The script will then close the page and fetch the recordings data, and organize the files by operator in the selected directory.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Selenium](https://selenium-python.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://docs.python-requests.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [webdriver_manager](https://pypi.org/project/webdriver-manager/)
