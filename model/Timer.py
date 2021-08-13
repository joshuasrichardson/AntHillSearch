import threading
import time
import pygame


class SimulationTimer:
    """ A class to keep track of the time remaining in the colony interface """

    def __init__(self, simulationDuration, timer, timeOut):
        self.simulationDuration = simulationDuration  # The duration of the interface in seconds
        self.timer = timer  # A timer to help keep track of how much time is left in the interface
        self.pauseTime = 0  # The time left when the interface was paused
        self.startTime = None  # The time when the interface was started
        self.timeOut = timeOut  # A method to call when the time runs out

    def start(self):
        self.startTime = time.time()
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def pause(self, handleEvent, collidesWithPlayButton):
        startPauseTime = time.time()
        remainingTime = self.getRemainingTime(startPauseTime)
        self.timer.cancel()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p or \
                        event.type == pygame.MOUSEBUTTONUP and collidesWithPlayButton(pygame.mouse.get_pos()):
                    paused = False
                else:
                    handleEvent(event)
        self.pauseTime += time.time() - startPauseTime
        self.timer = threading.Timer(remainingTime, self.timeOut)
        self.timer.start()

    def getRemainingTime(self, now):
        """ Returns the time left in the interface """
        if now is None:
            now = time.time()
        runTime = now - self.pauseTime - self.startTime
        remainingTime = self.simulationDuration - runTime
        return remainingTime
