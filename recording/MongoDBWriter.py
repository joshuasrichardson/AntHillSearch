import json

import pymongo

from Constants import CONFIG_FILE_NAME
from recording import MongoDBURL


class MongoDBWriter:
    def __init__(self):
        client = pymongo.MongoClient(MongoDBURL.getUrl())
        db = client.ants
        self.collection = db.empirical_testing

    def insert(self, results, world):
        with open(CONFIG_FILE_NAME, 'r') as configFile:
            configData = json.load(configFile)

        # Get the actual values in simulations where these values were generated randomly
        configData['HUB_RADII'] = f"{list(map(lambda hub: hub.radius, world.hubs))}"
        configData['HUB_POSITIONS'] = f"{list(map(lambda hub: hub.pos, world.hubs))}"
        configData['SITE_RADII'] = f"{list(map(lambda site: site.radius, world.siteList[len(world.hubs):]))}"
        configData['SITE_POSITIONS'] = f"{list(map(lambda site: site.pos, world.siteList[len(world.hubs):]))}"
        configData['SITE_QUALITIES'] = f"{list(map(lambda site: site.quality, world.siteList[len(world.hubs):]))}"
        configData['PRED_POSITIONS'] = f"{list(map(lambda pred: pred.pos, world.predatorList))}"

        mydict = {"config": configData,
                  "results": results}

        self.collection.insert_one(mydict)

    def find(self, query):
        return self.collection.find(query)


# a = MongoDBWriter()
# doc = a.find({})
# for x in doc:
#     print(x)
