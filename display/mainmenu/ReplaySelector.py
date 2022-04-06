import os

from config import Config
from display import Display
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.SelectorButton import SelectorButton
from display.mainmenu.buttons.Title import Title


class ReplaySelector(MenuScreen):

	def __init__(self):
		self.y = 50
		self.latestReplays = self.getLatestReplays()
		super().__init__([Title("Select a Replay", 90), BackButton(), *self.getReplayButtons()])
		self.option = ""

	def nextY(self):
		y = self.y
		self.y += 50
		return y

	@staticmethod
	def getLatestReplays():
		replays = [file for file in os.listdir('./recording/results/') if file.endswith('RECORDING.json')]
		os.chdir('./recording/results')
		replays.sort(key=os.path.getmtime, reverse=True)
		os.chdir('../..')
		latestReplays = []
		for replay in replays[:Config.NUM_REPLAYS]:
			latestReplays.append(replay)

		return latestReplays

	def getReplayButtons(self):
		""" Return buttons to display and return the most recent replays """
		replayButtons = []
		for replay in self.latestReplays:
			button = SelectorButton(self.formatReplayName(replay), replay, Display.origWidth / 3, self.nextY(), self)
			replayButtons.append(button)
		return replayButtons

	@staticmethod
	def formatReplayName(replay):
		if len(replay) == 35:
			return f"{replay[0:3]} {replay[4:6]}, {replay[7:11]} at {replay[12:14]}:{replay[15:17]}:{replay[18:20]}"
		elif len(replay) == 34:
			return f"{replay[0:3]} {replay[4:5]}, {replay[6:10]} at {replay[11:13]}:{replay[14:16]}:{replay[17:19]}"
		else:
			return replay

	def chooseReplay(self):
		super().run()
		return self.option
