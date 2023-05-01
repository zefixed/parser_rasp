import json
import configparser
from os import mkdir, listdir, walk
from datetime import datetime, date, timedelta
from shutil import copyfile, rmtree

settings_parser = configparser.ConfigParser()
settings_parser.read("settings_parser.ini")
data_file = settings_parser["settings"]["dest_file"]

settings_saver_deleter = configparser.ConfigParser()
settings_saver_deleter.read("settings_saver_deleter.ini")
groups = settings_saver_deleter["settings"]["groups"].split(", ")
mode = settings_saver_deleter["settings"]["mode"]

date_today = date.today()
date_time = ".".join(str(datetime.now()).split(":"))


def to_integer(dt_time):
    try:
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day
    except Exception as e:
        print(e)


match settings_saver_deleter["settings"]["mode"]:
    case "save":
        if len(groups) != 1:
            exit(f"Save mode taken only one group, given {len(groups)}")
    case "delete":
        if len(groups) < 1:
            exit(f"Delete mode taken more groups, given 0")
    case _:
        exit(f"Incorrect mode")

if mode == "save":
    group = groups[0]

    try:
        mkdir("dumps")
    except FileExistsError:
        print(f"Folder dumps is exists")

    try:
        mkdir(f".\\dumps\\{group}")
    except FileExistsError:
        print(f"\tFolder {group} is exists")

    try:
        mkdir(f".\\dumps\\{group}\\{date_today}")
    except FileExistsError:
        print(f"\t\tFolder {date_today} is exists")

    copyfile(f"{data_file}.json", f"dumps/{group}/{date_today}/{date_time}.json")

else:
    for group in groups:
        dirs = listdir(f".\\dumps\\{group}")

        for dir in dirs:
            ago_180 = to_integer(date_today - timedelta(180))
            if to_integer(datetime.strptime(dir, "%Y-%m-%d").date()) < ago_180:
                rmtree(f".\\dumps\\{group}\\{dir}")

