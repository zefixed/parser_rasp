import json
from playwright.sync_api import sync_playwright
import configparser

config = configparser.ConfigParser()
config.read("settings_parser.ini")

group = config["settings"]["group"]
url = f"https://rasp.dmami.ru/json/?{group}"


def rename(dct):
   pass


def trash_from_json(jsn):
    for day in jsn.values():
        for pairs in day.values():
            for pair in pairs:
                # deleting trash from json
                pair.pop("dts")
                pair.pop("auditories")
                pair.pop("week")
                pair.pop("align")
                pair.pop("e_link")

                # rename the elements

    return jsn


with sync_playwright() as p:
    def handle_response(response):
        if "/group?" in response.url:
            with open(config["settings"]["dest_file"] + ".json", 'w', encoding='utf-8') as f:
                json.dump(trash_from_json(response.json()["grid"]), f, ensure_ascii=False)

    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", handle_response)
    page.goto(url, wait_until="networkidle")
    page.context.close()
    browser.close()
