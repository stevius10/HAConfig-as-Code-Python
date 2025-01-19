from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.mappings import MAP_KEY_ERROR, MAP_KEY_IGNORE, MAP_KEY_RESULT

from .apartment import apartment_filter
from .scrape import fetch, scrape

def scrape_housing(provider):
    filtered = []
    ignored = []
    structure = DATA_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]
    try:
        content = fetch(provider)
        apartments = scrape(content, structure["item"], structure["address_selector"], 
                          structure["rent_selector"], structure["size_selector"], 
                          structure["rooms_selector"], structure["details_selector"])

        for apartment in apartments:
            if apartment_filter(apartment):
                del apartment['text']
                filtered.append(apartment)
            else:
                ignored.append(apartment)
                
        return filtered, ignored
    except Exception as e:
        return [type(Exception)], [str(e)]
