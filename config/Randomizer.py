import json

import Utils
import random

from Constants import CONFIG_FILE_NAME


class Setting:
    def __init__(self, key, minimum, maximum, isFloat=False, isBool=False, isArray=False, isPos=False, numValues=1):
        self.key = key
        numberInRange = random.uniform if isFloat else random.randint
        if isArray:
            self.value = [numberInRange(minimum, maximum) for _ in range(numValues)]
        elif isPos:
            self.value = [[numberInRange(minimum, maximum), numberInRange(minimum, maximum)]
                          for _ in range(numValues)]
        elif isBool:
            self.value = numberInRange(0, 1) == 1
        else:
            self.value = numberInRange(minimum, maximum)


def randomizeConfig():
    numSitesSetting = Setting("NUM_SITES", 2, 8)
    sitePosSetting = Setting("SITE_POSITIONS", -1500, 1500, isPos=True, numValues=numSitesSetting.value)
    distances = [Utils.getDistance([0, 0], pos) for pos in sitePosSetting.value]
    maxDist = max(distances)

    settings = [
        numSitesSetting,
        Setting("SITE_RADII", 20, 60, isArray=True, numValues=numSitesSetting.value),
        Setting("SITE_QUALITIES", 0, 255, isArray=True, numValues=numSitesSetting.value),
        sitePosSetting,
        Setting("HUB_AGENT_COUNTS", 20, 200, isArray=True),
        Setting("MAX_SEARCH_DIST", maxDist, maxDist + 300, isFloat=True),
        Setting("HOMOGENOUS_AGENTS", 0, 1, isBool=True),
        Setting("MIN_AGENT_SPEED", 4, 10),
        Setting("MAX_AGENT_SPEED", 11, 15),
        Setting("COMMIT_SPEED_FACTOR", 1, 3),
        Setting("MAX_FOLLOWERS", 1, 4),
        Setting("MIN_DECISIVENESS", 0.2, 1.0, isFloat=True),
        Setting("MAX_DECISIVENESS", 1.0, 2.5, isFloat=True),
        Setting("MIN_NAV_SKILLS", 0.01, 0.3, isFloat=True),
        Setting("MAX_NAV_SKILLS", 1.0, 3.0, isFloat=True),
        Setting("MIN_QUALITY_MISJUDGMENT", 0, 30),
        Setting("MAX_QUALITY_MISJUDGMENT", 30, 100),
        Setting("AT_NEST_THRESHOLD", 4, 8),
        Setting("SEARCH_THRESHOLD", 3, 6),
        Setting("SEARCH_FROM_HUB_THRESHOLD", 6, 10),
        Setting("MAX_ASSESS_THRESHOLD", 7, 11),
        Setting("ASSESS_DIVIDEND", 40, 60),
        Setting("GET_LOST_THRESHOLD", 4, 6),
        Setting("FOLLOW_THRESHOLD", 1, 2),
        Setting("LEAD_THRESHOLD", 3, 5),
        Setting("MIN_ACCEPT_VALUE", 20, 200),
        Setting("QUORUM_DIVIDEND", 5, 9),
    ]

    # for setting in settings:
    #     print(f"{setting.key}: {setting.value}")
    setKeysValues(settings)


def setKeysValues(settings):
    with open(CONFIG_FILE_NAME, 'r') as file:
        data = json.load(file)
    for setting in settings:
        data[setting.key] = setting.value
    with open(CONFIG_FILE_NAME, 'w') as file:
        json.dump(data, file)
    Utils.copyJsonToConfig()
