import numpy as np
from custom_types import Point2D
from MotionPlanner.planner import interpolate 
import random
def gauss_2d(mu, sigma):
	x = random.gauss(mu.x, sigma)
	y = random.gauss(mu.y, sigma)
	return Point2D(x, y).toInt()


class ConfigSpace2D():

	def __init__(self):
		self.initialConfig = None
		self.goalConfig = None
		self.configspace = None
		self.solutionPath = []
		self.start = None
		self.end = None
		self.max_config_x, self.max_config_y = None, None
	def reset(self):
		self.start = None
		self.end = None
	def getConfig_max(self):
		return self.max_config_x, self.max_config_y
	def setConfig_max(self, room_size, robot_size):
		self.max_config_x = room_size.width - robot_size.width
		self.max_config_y = room_size.height - robot_size.height
	def setInitial(self, point2d):
		self.start = point2d
	def setGoal(self, point2d):
		self.end = point2d
	def isGoalSet(self):
		if self.end is None:
			return False
		else:
			return True
	def isStartSet(self):
		if self.start is None:
			return False
		else:
			return True
	def CreateCspace(self, wspace, robot):
		pass
	def initSolutionPath(self, planner = None, samples=50, radius=50):
		if planner is None:
			self.solutionPath = interpolate(self.start, self.end, resolution = 0.1) 
		else:
			self.solutionPath = planner.shortestPath([(self.start, self.end)], samples=samples, radius=radius)
	def pathExistFrmSrcToDest(self):
		if self.solutionPath:
			return True
		else:
			return False
	def next_position(self):
		for i in range(len(self.solutionPath)):
			yield self.solutionPath[i]
	def PrintCspace(self):
		pass
	def PrintPath(self):
		pass
	def sample_config(self):
		x = np.random.randint(0, self.max_config_x)
		y = np.random.randint(0, self.max_config_y)
		return Point2D(x, y)
	def CSampleSpace(self, wspace, sample_type = 'uniform'):
		if sample_type == 'uniform':
			return self._cFreeSpace_uniform(wspace)
		elif sample_type == 'gaussian':
			return self._cFreeSpace_gaussian(wspace)
		elif sample_type == 'bridgetest':
			return self._cFreeSpace_bridgetest(wspace)
	def _cObsSpace_uniform(self, wspace):
		while True:
			configuration = self.sample_config()
			if wspace.IsInCollision(configuration):
				return configuration
	def _cFreeSpace_uniform(self, wspace):
		while True:
			configuration = self.sample_config() 
			if not wspace.IsInCollision(configuration):
				return configuration
	def _cFreeSpace_gaussian(self, wspace):
		sigma = 40
		while True:
			c1 = self._cObsSpace_uniform(wspace)
			c2 = gauss_2d(c1, sigma)
			if not wspace.IsInCollision(c2):
				return c2
	def _cFreeSpace_bridgetest(self, wspace):
		sigma = 40
		while True:
			c1 = self.sample_config()
			if wspace.IsInCollision(c1):
				c2 = gauss_2d(c1,sigma)
				if wspace.IsInCollision(c2):
					vec = (c2 - c1) * 0.5
					p = c1 + vec.toInt()
					if not wspace.IsInCollision(p):
						return p

		