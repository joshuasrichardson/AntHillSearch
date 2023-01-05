""" Functions for converting json files or objects to csv files """
import json
import csv
import os
from datetime import datetime

from Constants import RESULTS_DIR
from config import Config


def jsonToCsv(json_file_name, out_file_name, should_separate=True):
    with open(json_file_name, 'r') as json_file:
        json_data = json.load(json_file)

    jsonObjectToCsv(json_data, out_file_name, should_separate)


def jsonObjectToCsv(json_data, out_file_name, should_separate=True):
    json_data['time_stamp'] = datetime.now()

    # Create the folder with the results if it does not exist
    path = f'{RESULTS_DIR}{Config.INTERFACE_NAME}'
    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)

    if not out_file_name.endswith('.csv'):
        out_file_name += '.csv'

    file_path = f'{path}/{out_file_name}'
    file_exists = os.path.exists(file_path)
    data_file = open(file_path, 'a', newline='')

    csv_writer = csv.writer(data_file)
    if not file_exists:  # If we just created the file, we need to add the headers
        csv_writer.writerow(json_data.keys())

    if should_separate:
        rows = separateIntoRows(json_data.values())
        for row in rows:
            csv_writer.writerow(row)
    else:
        csv_writer.writerow(json_data.values())

    data_file.close()


def separateIntoRows(values):
    rows = []
    for value in values:
        if type(value) == list:
            if len(value) == 0:
                if len(rows) <= 0:
                    rows.append([])
                for row in rows:
                    row.append(None)
            for rowIndex, item in enumerate(value):
                if len(rows) <= rowIndex:
                    rows.append([])
                rows[rowIndex].append(item)
        else:
            if len(rows) <= 0:
                rows.append([])
            for row in rows:
                row.append(value)
    return rows


def insert(results, world):
    # prepend with config or results to match the mongodb csv files' format
    dictionary = {
        "config.NUM_SITES": len(world.siteList) - len(world.hubs),
        "config.SITE_POSITIONS": f"{list(map(lambda site: site.pos, world.siteList[len(world.hubs):]))}",
        'config.SITE_QUALITIES': f"{list(map(lambda site: site.quality, world.siteList[len(world.hubs):]))}",
        'results.NUM_ROUNDS': results["NUM_ROUNDS"],
        'results.CHOSEN_HOME_QUALITIES': results["CHOSEN_HOME_QUALITIES"],
        'results.CHOSEN_HOME_POSITIONS': results["CHOSEN_HOME_POSITIONS"],
        'results.NUM_ARRIVALS': results["NUM_ARRIVALS"],
        'results.TOTAL_AGENTS': results["TOTAL_AGENTS"]
    }

    if Config.RESULTS_FILE_NAME is not None:
        jsonObjectToCsv(dictionary, Config.RESULTS_FILE_NAME, should_separate=False)
