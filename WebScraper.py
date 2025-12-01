import requests
from bs4 import BeautifulSoup
import time
import json
import re

# Retry mechanism and data scraping function
def fetch_data_with_retries(url, retries=3, delay=2):
    """
    fetches data from a URL with retry mechanism in case of failures
    """

    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                raise

# Function to scrape data from a webpage using BeautifulSoup and regex
def extract_data_from_html(html_content):
    """
    Extracting the relevent data (links containing 'python') from the HTML content 
    """
    if not html_content:
        raise ValueError("HTML content is empty!!!")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = []

    # Regex pattern to find links containing 'python'
    for link in soup.find_all('a', href=True):
        title = link.get_text()
        if re.match(r'.*python.*', title, re.IGNORECASE): #looking for 'python' in the link text
            titles.append(title)

    return titles

# Function to save extracted data to a JSON file
def save_data_to_json(data, filename='extracted_data.json'):
    """
    Saves the extracted data to a JSON file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")


# Url to scrape data from
url = 'https://docs.python.org/3/'

# Fetch, ectract and save data
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)