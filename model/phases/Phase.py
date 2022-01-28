from abc import ABC, abstractmethod


class Phase(ABC):
    """ Agent phases or levels of commitment on their way to finding the best new site """

    @abstractmethod
    def getNumber(self):
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return uncommittedSpeed * speedCoefficient
