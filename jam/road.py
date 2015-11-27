import logging
from collections import defaultdict

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
			if len(line1) > 1:
				self.lines.append(line1)
			else:
				logging.error("%s sort failed: %s", self.name, len(sections))
				break
		for num,line in enumerate(self.lines):
			# for sect in line:
			# 	logging.debug(sect.points)
			logging.debug("%s line %d: %d", self.name, num, len(line))

	def top_left(self):
		points = [RoadSection.top_left(line) for line in self.lines]
		#logging.debug("%s: %s", self.name, points)
		self.tl_point = top_left(points)
		return self.tl_point

	def bottom_right(self):
		points = [RoadSection.bottom_right(line) for line in self.lines]
		#logging.debug("%s: %s", self.name, points)
		self.br_point = bottom_right(points)
		return self.br_point

	def convert_points(self, mapinfo):
		for ln in self.lines:
			for s in ln:
				s.convert_points(mapinfo)
		self.tl_point = convert_point(self.tl_point, mapinfo)
		self.br_point = convert_point(self.br_point, mapinfo)

	def calc_middle(self):
		self.middle = Point(x=(self.tl_point.x + self.br_point.x) // 2,
							y=(self.tl_point.y + self.br_point.y) // 2)
		return self.middle

	def judge_horiz(self):
		s0 = self.lines[0][0]
		s1 = self.lines[0][-1]
		p0 = s0.points[0]
		p1 = s1.points[-1]
		return (p1.x - p0.x) > (p1.y - p0.y)

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
			points = [s.points[0] for s in ln]
			points.append(ln[-1].points[-1])
			dlines.append(points)
		return dlines

	@staticmethod
	def top_left_corner(roads):
		points = [roads[name].top_left() for name in roads]
		return top_left(points)

	@staticmethod
	def bottom_right_corner(roads):
		points = [roads[name].bottom_right() for name in roads]
		return bottom_right(points)

	@staticmethod
	def parse_roads(roads_sections):
		roads = {}
		for name in roads_sections:
			roads[name] = Road(name, roads_sections[name])
		return roads