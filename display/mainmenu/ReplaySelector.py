import os

from config import Config
from display import Display
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.Title import Title
from display.buttons.BackButton import BackButton
from display.buttons.SelectorButton import SelectorButton


class ReplaySelector(MenuScreen):
	""" The screen that allows the user to choose which of the most recent replays they would like to view """

	def __init__(self):
		self.y = Display.origHeight / 3
		self.latestReplays = self.getLatestReplays()
		super().__init__([Title("Select a Replay", 200), BackButton(), *self.getReplayButtons()])
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
			button = SelectorButton(self.formatReplayName(replay), replay, Display.origWidth * 2 / 5, self.nextY(), self)
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
