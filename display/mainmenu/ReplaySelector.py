import os

import pygame
from pygame import MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, K_ESCAPE, QUIT

from config import Config
from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, WORDS_COLOR, BLUE
from display import Display
from interface.EngineerInferface import EngineerInterface
from interface.UserInterface import UserInterface


class ReplaySelector:

	def __init__(self):
		self.numReplays = Config.NUM_REPLAYS
		self.y = 100
		self.latestReplays = self.getLatestReplays(self.numReplays)
		self.font = pygame.font.SysFont('Comic Sans MS', Config.LARGE_FONT_SIZE)
		self.latestReplayImages = self.getLatestReplayImages()
		self.latestReplayButtons = self.getLatestReplayButtons()
		self.replay = None

	def nextY(self):
		y = self.y
		self.y -= 50
		return y

	def getLatestReplays(self, numReplays):
		replays = [file for file in os.listdir('./recording/results/') if file.endswith('RECORDING.json')]
		os.chdir('./recording/results')
		replays.sort(key=os.path.getmtime, reverse=True)
		os.chdir('../..')
		latestReplays = []
		for replay in replays[:numReplays]:
			latestReplays.append(replay)

		return latestReplays

	def getLatestReplayImages(self):
		replayImages = []
		for i in range(self.numReplays):
			image = self.font.render(self.latestReplays[i], True, WORDS_COLOR).convert_alpha()
			replayImages.append(image)
		return replayImages

	def getLatestReplayButtons(self):
		replayButtons = []
		for i in range(self.numReplays):
			image = self.latestReplayImages[i]
			button = pygame.Rect((Display.origWidth / 2) - (image.get_width() / 2), (Display.origHeight / 2) - self.nextY(), image.get_width(), image.get_height())
			print(f"i: {i}")
			print(f"button: {button}")
			replayButtons.append(button)
		return replayButtons

	def chooseReplay(self):
		print(f"latestReplays: {self.latestReplays}")
		print(f"latestReplayImages: {self.latestReplayImages}")
		print(f"latestReplayButtons: {self.latestReplayButtons}")
		reading = True
		while reading:
			Display.screen.fill(SCREEN_COLOR)
			for i in range(len(self.latestReplayImages)):
				Display.blitImage(Display.screen, self.latestReplayImages[i], self.latestReplayButtons[i].topleft, False)
			pygame.display.flip()
			reading = self.handleEvents()
		return self.replay

	def handleEvents(self):
		""" Handle user input """
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				return self.mouseButtonPressed(pygame.mouse.get_pos())
			elif event.type == MOUSEMOTION:
				self.updateCursor()
				self.updateWords(pygame.mouse.get_pos())
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				self.replay = None
				return False
			if event.type == QUIT:
				pygame.quit()
				raise GameOver("Game Over")
		return True

	def mouseButtonPressed(self, pos):
		for i in range(len(self.latestReplayButtons)):
			if self.latestReplayButtons[i].collidepoint(pos):
				self.replay = self.latestReplays[i]
				return False
		return True

	def updateWords(self, pos):
		for i in range(len(self.latestReplayButtons)):
			if self.latestReplayButtons[i].collidepoint(pos):
				self.latestReplayImages[i] = self.font.render(self.latestReplays[i], True, BLUE).convert_alpha()
			else:
				self.latestReplayImages[i] = self.font.render(self.latestReplays[i], True, WORDS_COLOR).convert_alpha()

	def updateCursor(self):
		cursorStyle = pygame.SYSTEM_CURSOR_HAND if self.collidesWithSelectable(pygame.mouse.get_pos()) \
			else pygame.SYSTEM_CURSOR_ARROW
		pygame.mouse.set_cursor(cursorStyle)

	def collidesWithSelectable(self, pos):
		return [replayButton.collidepoint(pos) for replayButton in self.latestReplayButtons]
