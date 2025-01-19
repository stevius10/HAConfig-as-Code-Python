import re

from constants.settings import (
    SET_SCRAPE_HOUSING_BLACKLIST,
    SET_SCRAPE_HOUSING_FILTER_AREA,
    SET_SCRAPE_HOUSING_FILTER_ROOMS,
    SET_SCRAPE_HOUSING_FILTER_RENT,
    SET_SCRAPE_HOUSING_FILTER_SQM_PRICE,
    SET_SCRAPE_HOUSING_FILTER_PLZ
)

from utils import *

@debugged
def apartment_create(address, rent=None, size=None, rooms=None, text=None):
    return {
        "address": address,
        "rent": rent,
        "size": size,
        "rooms": rooms,
        "text": text,
    }

def apartment_compare(apartment, address, rent=None, size=None, rooms=None):
    return (
        apartment.get("address") == address
        and (rent is None or apartment.get("rent") == rent)
        and (size is None or apartment.get("size") == size)
        and (rooms is None or apartment.get("rooms") == rooms)
    )

def apartment_string(a):
  details = ", ".join([x for x in [f"{str(a.get('rent'))}€" if a.get("rent") else None, f"{str(a.get('size'))}m²" if a.get("size") else None, f"{str(a.get('rooms'))}Z." if a.get("rooms") else None] if x])
  return f"{a['address']} ({details})" if details else a["address"]

@debugged
def apartment_filter(a):
    if not is_rent_in_range(a):
        return False
    if not is_size_in_range(a):
        return False
    if not is_rooms_in_range(a):
        return False
    if not is_sqm_below_threshold(a):
        return False
    if has_invalid_plz(a):
        return False
    if is_blacklisted(a):
        return False
    return True

def is_rent_in_range(a):
    if a["rent"] and re.findall(r"\d", a["rent"]):
        rent_value = int("".join(re.findall(r"\d", a["rent"])[:3]))
        return 400 < rent_value < SET_SCRAPE_HOUSING_FILTER_RENT
    return True

def is_size_in_range(a):
    if a["size"] and re.findall(r"\d", a["size"]):
        size_value = int("".join(re.findall(r"\d", a["size"])[:3]))
        return SET_SCRAPE_HOUSING_FILTER_AREA <= size_value
    return True

def is_rooms_in_range(a):
    if a["rooms"] and re.findall(r"\d", a["rooms"]):
        rooms_value = int("".join(re.findall(r"\d", a["rooms"])[:2]))
        return SET_SCRAPE_HOUSING_FILTER_ROOMS <= rooms_value
    return True

def is_sqm_below_threshold(a):
    if a["rent"] and a["size"]:
        rent_value = int("".join(re.findall(r"\d", a["rent"])[:3]))
        size_value = int("".join(re.findall(r"\d", a["size"])[:3]))
        if size_value > 0:
            sqm_price = rent_value / size_value
            return sqm_price < SET_SCRAPE_HOUSING_FILTER_SQM_PRICE
    return True

def has_invalid_plz(a):
    if a["address"]:
        plz_match = re.search(r"\b\d{5}\b", a["address"])
        return plz_match and plz_match.group() not in SET_SCRAPE_HOUSING_FILTER_PLZ
    return False

def is_blacklisted(a):
    if a["text"]:
        for item in SET_SCRAPE_HOUSING_BLACKLIST:
            if re.search(r"\b" + re.escape(item.lower()) + r"\b", a["text"].lower()):
                return True
        return False
    return False
