import json
from playwright.sync_api import sync_playwright
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

group = config["settings"]["group"]
url = f"https://rasp.dmami.ru/json/?{group}"

with sync_playwright() as p:
    def handle_response(response):
        if "/group?" in response.url:
            with open(config["settings"]["dest_file"], 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False)

    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", handle_response)
    page.goto(url, wait_until="networkidle")
    page.context.close()
    browser.close()
