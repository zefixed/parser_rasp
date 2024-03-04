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


def rename_json_keys(jsn):
    new_days = {
        "1": "monday",
        "2": "tuesday",
        "3": "wednesday",
        "4": "thursday",
        "5": "friday",
        "6": "saturday",
    }

    new_pairs = {
        "1": "first",
        "2": "second",
        "3": "third",
        "4": "fourth",
        "5": "fifth",
        "6": "sixth",
        "7": "seventh",
    }

    new_jsn = {}
    for weekday in jsn:
        new_jsn[new_days[weekday]] = jsn[weekday]

    for day_key in new_jsn:
        for old_pair_key in new_pairs:
            tmp = new_jsn[day_key][old_pair_key]
            new_jsn[day_key][new_pairs[old_pair_key]] = tmp
            new_jsn[day_key].pop(old_pair_key)

    return new_jsn

with sync_playwright() as p:
    def handle_response(response):
        if "/group?" in response.url:
            with open(config["settings"]["dest_file"] + ".json", 'w', encoding='utf-8') as f:
                json.dump(rename_json_keys(trash_from_json(response.json()["grid"])), f, ensure_ascii=False)
                

    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", handle_response)
    page.goto(url, wait_until="networkidle")
    page.context.close()
    browser.close()
