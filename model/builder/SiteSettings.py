siteNoCloserThan = 0  # The closest to the hub a site can randomly be generated
siteNoFartherThan = 0  # The furthest to the hub a site can randomly be generated
hubCanMove = False  # Whether the hub can be moved by the user


def setSettings(noCloser, noFarther, hCanMove):
    global siteNoCloserThan
    siteNoCloserThan = noCloser
    global siteNoFartherThan
    siteNoFartherThan = noFarther
    global hubCanMove
    hubCanMove = hCanMove
