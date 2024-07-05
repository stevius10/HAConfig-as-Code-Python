from constants.expressions import EXPR_TIME_SERVICE_FILEBACKUP
from constants.secrets import SEC_DEVICES
from constants.settings import SET_SUBPROCESS_FILEBACKUP_FOLDER, SET_SUBPROCESS_FILEBACKUP_RETENTION, \
  SET_SCRAPE_HOUSING_FILTER_AREA, SET_SCRAPE_HOUSING_FILTER_RENT, SET_SCRAPE_HOUSING_FILTER_ROOMS
from utils import expr

# Automation

DATA_DEVICES = {
    "home": [{"id": entry["id"], "default": entry["default"]} for entry in SEC_DEVICES["home"]],
    "mobile": [{"id": entry["id"], "default": entry["default"]} for entry in SEC_DEVICES["mobile"]]
}

DATA_PRESENCE = {
  "wohnzimmer": {
    "on": [],
    "off": [
      { "condition": expr("state.get('climate.wohnzimmer')", "'on'"),
        "action": lambda: [service.call("climate", "turn_off", entity_id=["climate.wohnzimmer"])] }
    ]
  },
  "schlafzimmer": {
    "on": [],
    "off": [
      { "condition": expr("state.get('climate.schlafzimmer')", "'on'"),
        "action": lambda: [service.call("climate", "turn_off", entity_id=["climate.schlafzimmer"])] }
    ]
  },
  "away": {
    "on": [
      { "condition": expr(["state.get('climate.wohnzimmer')", "state.get('climate.schlafzimmer')"], "'on'", operator='or'),
        "action": lambda: [service.call("climate", "turn_off", entity_id=["climate.wohnzimmer", "climate.schlafzimmer"])] }
    ],
    "off": []
  }
}

DATA_SUBPROCESS_SERVICES = {
  "compile": {
    "commands": [
      "cd /config",
      "git ls-files -oc --exclude-standard",
      "git ls-files -oc --exclude-standard | grep -v '^www/' | while read -r file; do echo -e '# $file\n'; cat $file; echo -e '\n---\n'; done"
    ]
  },
  "backup": {
    "commands": [
      "apk add rsync; ulimit -n 4096",
      f"backup_folder=\"{SET_SUBPROCESS_FILEBACKUP_FOLDER}/$(date +\"%d-%m-%Y\")\"",
      f"/usr/bin/find {SET_SUBPROCESS_FILEBACKUP_FOLDER} -type f -mtime +{SET_SUBPROCESS_FILEBACKUP_RETENTION} -delete 2>&1",
      f"/usr/bin/find {SET_SUBPROCESS_FILEBACKUP_FOLDER} -mindepth 1 -maxdepth 1 -mtime +{SET_SUBPROCESS_FILEBACKUP_RETENTION} -type d -exec rm -r \"{{}}\" \\; 2>&1",
      f"rsync -av --exclude='.git/' --exclude='/homeassistant/.git/' --exclude='.storage/xiaomi_miot' --exclude='/homeassistant/.storage/xiaomi_miot' /config/ {SET_SUBPROCESS_FILEBACKUP_FOLDER} 2>&1"
    ],
    "trigger": EXPR_TIME_SERVICE_FILEBACKUP
  }
}

# Application

DATA_SCRAPE_HOUSING_PROVIDERS = {
  "degewo": { "url": f"https://immosuche.degewo.de/de/search?size=10&page=1&property_type_id=1&categories%5B%5D=1&lat=&lon=&area=&address%5Bstreet%5D=&address%5Bcity%5D=&address%5Bzipcode%5D=&address%5Bdistrict%5D=&district=33%2C+46%2C+28%2C+29%2C+60&property_number=&price_switch=true&price_radio={SET_SCRAPE_HOUSING_FILTER_RENT}-warm&price_from=&price_to=&qm_radio=SERVICE_SCRAPE_HOUSING_FILTER_AREA&qm_from={SET_SCRAPE_HOUSING_FILTER_ROOMS}&qm_to=&rooms_radio=custom&rooms_from=&rooms_to=&wbs_required=&order=rent_total_without_vat_asc",
              "structure": { "item": ".properties-container .property-container", "address_selector": ".property-subtitle", "rent_selector": ".property-rent", "size_selector": ".property-size", "rooms_selector": ".property-rooms", "details_selector": ".property-actions a"  } },
  "friedrichsheim": { "url": "https://www.friedrichsheim-eg.de/category/freie-wohnungen/",
                      "structure": { "item": "#main h2.entry-title", "address_selector": "*", "rent_selector": None, "size_selector": None, "rooms_selector": None, "details_selector": None } },
  "howoge": { "url": "https://www.howoge.de/immobiliensuche/wohnungssuche.html?tx_howrealestate_json_list%5Bpage%5D=1&tx_howrealestate_json_list%5Blimit%5D=12&tx_howrealestate_json_list%5Blang%5D=&tx_howrealestate_json_list%5Brooms%5D=&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Charlottenburg-Wilmersdorf&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Neukoelln&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Tempelhof-Schöneberg&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Mitte&tx_howrealestate_json_list%5Bkiez%5D%5B%5D=Friedrichshain-Kreuzberg",
              "structure": { "item": ".tx-howsite-flats .list-entry", "address_selector": ".address", "rent_selector": ".price", "size_selector": None, "rooms_selector": ".rooms", "details_selector": ".wbs" } },


  "ibw": { # approved 280624
      "url": "https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php",
      "structure": {"item": "span._tb_left", "address_selector": None, "rent_selector": None, "size_selector": None, "rooms_selector": None, "details_selector": None },
      "request_headers": { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest' }, "request_data": { 'q': 'wf-save-srch', 'save': 'false', 'qm_min': SET_SCRAPE_HOUSING_FILTER_AREA, 'miete_max': SET_SCRAPE_HOUSING_FILTER_RENT, 'rooms_min': SET_SCRAPE_HOUSING_FILTER_ROOMS, 'bez[]': ['01_00', '02_00', '03_00', '04_00', '02_00'], 'wbs': 1 } },

  "gewobag": { # approved 210624
      "url": f"https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis={SET_SCRAPE_HOUSING_FILTER_RENT}&gesamtflaeche_von={SET_SCRAPE_HOUSING_FILTER_AREA}&gesamtflaeche_bis=&zimmer_von={SET_SCRAPE_HOUSING_FILTER_ROOMS}&zimmer_bis=&keinwbs=0&sort-by=recent",
      "structure": { "item": ".filtered-mietangebote .angebot-content", "address_selector": "address", "rent_selector": ".angebot-kosten td", "size_selector": ".angebot-area td", "rooms_selector": "", "details_selector": ".angebot-title" } },

  "wbm": { # approved 190624
      "url": "https://www.wbm.de/wohnungen-berlin/angebote/",
      "structure": { "item": ".openimmo-search-list-item", "address_selector": ".address", "rent_selector": ".main-property-rent", "size_selector": ".main-property-size", "rooms_selector": ".main-property-rooms", "details_selector": "h2 .check-property-list" } }
}

