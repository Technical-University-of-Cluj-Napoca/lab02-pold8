import sys
import requests
from bs4 import BeautifulSoup

def define(word: str) -> str:
    BASE_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/"
    url = BASE_URL + word.lower()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    soup = BeautifulSoup(response.content,  'html.parser')

    entry = soup.find('div', class_='entry')

    if entry:
        definition = entry.find('span', class_='def')

        if definition:
            definition_text = definition.get_text(separator=' ', strip=True)
            return definition_text
        else:
            return f"Definition not found"
    return f"No main entry found"