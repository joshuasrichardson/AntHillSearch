import Constants
from Constants import *


maxSearchDistance = Constants.MAX_SEARCH_DIST  # The farthest distance an agent can go away from their assigned hub while searching
findAssignedSiteEasily = FIND_SITES_EASILY  # Whether agents know where sites are after they have moved
commitSpeedFactor = COMMIT_SPEED_FACTOR  # How many times faster the agents get when they commit
homogenousAgents = HOMOGENOUS_AGENTS
minSpeed = MIN_AGENT_SPEED
maxSpeed = MAX_AGENT_SPEED
minDecisiveness = MIN_DECISIVENESS
maxDecisiveness = MAX_DECISIVENESS
minNavSkills = MIN_NAV_SKILLS
maxNavSkills = MAX_NAV_SKILLS
minEstAccuracy = MIN_QUALITY_MISJUDGMENT
maxEstAccuracy = MAX_QUALITY_MISJUDGMENT


def setSettings(homogenous=HOMOGENOUS_AGENTS, minSp=MIN_AGENT_SPEED, maxSp=MAX_AGENT_SPEED,
                minDec=MIN_DECISIVENESS, maxDec=MAX_DECISIVENESS, minNav=MIN_NAV_SKILLS,
                maxNav=MAX_NAV_SKILLS, minEst=MIN_QUALITY_MISJUDGMENT, maxEst=MAX_QUALITY_MISJUDGMENT,
                msd=MAX_SEARCH_DIST, fse=FIND_SITES_EASILY, csf=COMMIT_SPEED_FACTOR):
    global homogenousAgents
    homogenousAgents = homogenous
    global minSpeed
    minSpeed = minSp
    global maxSpeed
    maxSpeed = maxSp
    global minDecisiveness
    minDecisiveness = minDec
    global maxDecisiveness
    maxDecisiveness = maxDec
    global minNavSkills
    minNavSkills = minNav
    global maxNavSkills
    maxNavSkills = maxNav
    global minEstAccuracy
    minEstAccuracy = minEst
    global maxEstAccuracy
    maxEstAccuracy = maxEst
    global maxSearchDistance
    maxSearchDistance = msd
    global findAssignedSiteEasily
    findAssignedSiteEasily = fse
    global commitSpeedFactor
    commitSpeedFactor = csf
