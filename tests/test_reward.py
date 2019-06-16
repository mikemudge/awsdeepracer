# import prevent_zig_zag as model
import unittest
import mudge_v1 as model
from nose.tools import assert_equals

class TestReward(unittest.TestCase):
	DEFAULT_PARAMS = {
		'x': 2.5,
		'y': 1.5,
		'distance_from_center': 0,
		'track_width': 30,
		'steering_angle': 0,
		'heading': 0,
		'waypoints': [[2.5, 1.5], [2.6, 1.5]],
		'closest_waypoints': [0, 1],
		'speed': 1,
	}

	def setUp(self):
		self.model = model
		self.params = self.DEFAULT_PARAMS.copy()

	def testWithBasicParams(self):
		r = self.model.reward_function(self.params)

		self.assertGreater(r, 0)

	def testOffCenter(self):
		self.params['distance_from_center'] = 7;

		r = self.model.reward_function(self.params)

		self.assertGreater(r, 0)

	def testLargeOffCenter(self):
		self.params['distance_from_center'] = 15;

		r = self.model.reward_function(self.params)

		self.assertGreater(r, 0)

	def testOffTrack(self):
		self.params['distance_from_center'] = 30;

		r = self.model.reward_function(self.params)

		self.assertGreater(r, 0)

	def testWayPointLoop(self):
		self.params['closest_waypoints'] = [1, 0]

		r = self.model.reward_function(self.params)

		self.assertGreater(r, 0)
