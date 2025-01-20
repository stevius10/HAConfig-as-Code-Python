import json
import regex as re
import requests
from bs4 import BeautifulSoup

from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS

from .apartment import *

from utils import *

providers = DATA_SCRAPE_HOUSING_PROVIDERS

def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
    apartments: List[Dict] = []
    elements = content.select(item)
    for element in elements:
        element_text = element.get_text(strip=True)

        address = get_or_default(element, address_selector)
        if not address:
            address_match = re.search(r'([A-Za-zäöüß\s.-]+\s\d+(?:,\s*[A-Za-zäöüß\s-]+)?)', element_text)
            address = address_match.group(1) if address_match else None
            address = re.split(r',', address)[0].strip()
        if address:
            match = re.match(r'([A-Za-zäöüß\s.-]+)\s(\d+)', address)
            if match:
                address = f"{match.group(1).strip()} {match.group(2).strip()}"

        rent = get_or_default(element, rent_selector)
        if not rent:
            rent_match = re.search(r'(\d+(?:,\d+)?)\s*€', element_text)
            rent = rent_match.group(1) if rent_match else None
        if rent:
            rent = re.search(r'\d+', rent).group()

        size = get_or_default(element, size_selector)
        if not size:
            size_match = re.search(r'(\d+(?:,\d+)?)\s*m²', element_text)
            size = size_match.group(1) if size_match else None
        if size:
            size = re.search(r'\d+', size).group()

        rooms = get_or_default(element, rooms_selector)
        if not rooms:
            rooms_match = re.search(r'(\d+(?:,\d+)?)\s*Zimmer', element_text)
            rooms = rooms_match.group(1) if rooms_match else None

        text = get_or_default(element, details_selector) or element_text
        plz = re.search(r'\b1\d{4}\b', address)

        if not ([rent, size, rooms].count(None) == 3 or address is None):
          apartments.append(apartment_create(address=address, rent=rent, size=size, rooms=rooms, text=text))

    return apartments

@pyscript_executor
def fetch(provider):
    if providers[provider].get("request_headers") and providers[provider].get("request_data"):
        response = requests.post(providers[provider]["url"], headers=providers[provider]["request_headers"], data=providers[provider]["request_data"], verify=False).text
        content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
    else:
        response = requests.get(providers[provider]["url"], verify=False)
        content = BeautifulSoup(response.content, 'html.parser')
    return content

# Format

def get_or_default(element, selector, default=None):
    if not selector:
        return default
        item = element.select_one(selector)
        return item.get_text().strip() if item else default
    elif callable(selector):
        return selector(element)
    return default
