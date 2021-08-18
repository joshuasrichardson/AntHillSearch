from Constants import *


maxSearchDistance = MAX_SEARCH_DIST  # The farthest distance an agent can go away from their assigned hub while searching
findAssignedSiteEasily = False  # Whether agents know where sites are after they have moved
commitSpeedFactor = 3  # How many times faster the agents get when they commit


class AgentSettings:

    def __init__(self, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED, maxSpeed=MAX_AGENT_SPEED,
                 minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS, minNavSkills=MIN_NAV_SKILLS,
                 maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT, maxEstAccuracy=MAX_QUALITY_MISJUDGMENT,
                 msd=MAX_SEARCH_DIST, fse=FIND_SITES_EASILY, csf=COMMIT_SPEED_FACTOR):
        self.homogenousAgents = homogenousAgents
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.minDecisiveness = minDecisiveness
        self.maxDecisiveness = maxDecisiveness
        self.minNavSkills = minNavSkills
        self.maxNavSkills = maxNavSkills
        self.minEstAccuracy = minEstAccuracy
        self.maxEstAccuracy = maxEstAccuracy

        global maxSearchDistance
        maxSearchDistance = msd
        global findAssignedSiteEasily
        findAssignedSiteEasily = fse
        global commitSpeedFactor
        commitSpeedFactor = csf
