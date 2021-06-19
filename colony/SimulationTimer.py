import threading
import time

import pygame


class SimulationTimer:

    def __init__(self, simulationDuration, timer, timeOut):
        self.simulationDuration = simulationDuration
        self.timer = timer
        self.pauseTime = 0
        self.startTime = None
        self.timeOut = timeOut

    def start(self):
        self.startTime = time.time()
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def pause(self, handleEvent):
        startPauseTime = time.time()
        runTime = startPauseTime - self.pauseTime - self.startTime
        remainingTime = self.simulationDuration - runTime
        print("Remaining time: " + str(remainingTime))
        self.timer.cancel()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False
                else:
                    handleEvent(event)
        self.pauseTime += time.time() - startPauseTime
        self.timer = threading.Timer(remainingTime, self.timeOut)
        self.timer.start()
