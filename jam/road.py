import logging
from collections import defaultdict
from functools import reduce

from .section import *


class CharPosition(object):

	def __init__(self, char):
		self.char = char
		self.pos = (0,0)

	def set_pos(self, index, total, middle, horiz=True):
		mid = total // 2 + 1
		x, y = middle.x, middle.y
		if horiz:
			x += (index - mid) * 24
			y += 10
		else:
			x += 10
			y += (index - mid) * 24
		self.pos = (x, y)


class Road():

	def __init__(self, name, sections):
		self.name = name
		self.lines = []
		self.chars_pos = []
		self.parse_sections(sections)

	def parse_sections(self, sections):
		while sections:
			line1 = sorted_sections(sections)
			if line1:
				self.lines.append(line1)
			else:
				logging.error("%s sort failed: %s", self.name, len(sections))
				break
		for num,line in enumerate(self.lines):
			# for sect in line:
			# 	logging.debug("%s %s", sect.id, sect.points)
			logging.debug("%s line %d: %d", self.name, num, len(line))

	def top_left(self):
		points = [RoadSection.top_left(line) for line in self.lines]
		return top_left(points)

	def bottom_right(self):
		points = [RoadSection.bottom_right(line) for line in self.lines]
		return bottom_right(points)

	# def convert_points(self, mapinfo):
	# 	for ln in self.lines:
	# 		for s in ln:
	# 			s.convert_points(mapinfo)
	# 	self.tl_point = convert_point(self.tl_point, mapinfo)
	# 	self.br_point = convert_point(self.br_point, mapinfo)

	def calc_middle(self):
		tl_point = self.top_left()
		br_point = self.bottom_right()
		self.middle = Point(x=(tl_point.x + br_point.x) // 2,
							y=(tl_point.y + br_point.y) // 2)
		return self.middle

	def judge_horiz(self):
		tl = self.top_left()
		br = self.bottom_right()
		width = br.x - tl.x
		height = br.y - tl.y
		logging.debug("%s is %s", self.name, ('horizontal' if width > height else 'vertical'))
		return width > height

	def set_name_pos(self):
		self.calc_middle()
		horiz = self.judge_horiz()
		logging.debug("%s horiz=%s", self.name, horiz)
		for i, c in enumerate(self.name):
			pos = CharPosition(c)
			pos.set_pos(i, len(self.name), self.middle, horiz)
			self.chars_pos.append(pos)

	def display_lines(self):
		dlines = []
		for ln in self.lines:
			points = reduce(lambda x,y: x + y[1:], [s.points for s in ln])
			dlines.append(points)
		return dlines

	# @staticmethod
	# def top_left_corner(roads):
	# 	points = [roads[name].top_left() for name in roads]
	# 	return top_left(points)

	# @staticmethod
	# def bottom_right_corner(roads):
	# 	points = [roads[name].bottom_right() for name in roads]
	# 	return bottom_right(points)

	@staticmethod
	def make_roads(grouped_sections):
		roads = {}
		for name in grouped_sections:
			roads[name] = Road(name, grouped_sections[name])
		return roads