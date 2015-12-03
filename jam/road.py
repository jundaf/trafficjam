import logging
from collections import defaultdict
from functools import reduce

from .section import *

CHAR_SIZE = 24

class CharPosition(object):

	def __init__(self, index, char, total):
		self.index = index
		self.char = char
		self.total = total
		self.pos = (0,0)

	def set_pos(self, middle, horiz=True):
		mid = self.total // 2 + 1
		x, y = middle.x, middle.y
		if horiz:
			x += (self.index - mid) * CHAR_SIZE
			y += 10
		else:
			x += 10
			y += (self.index - mid) * CHAR_SIZE
		self.pos = (x, y)

	def set_pos_head(self, head, horiz=True):
		x, y = head.x, head.y
		if horiz:
			x += (self.index + 2) * CHAR_SIZE
			y += 10
		else:
			x += 15
			y += (self.index + 2) * CHAR_SIZE
		self.pos = (x, y)


class Road():

	def __init__(self, name, sections):
		self.name = name
		self.lines = []
		self.chars_pos = []
		self.parse_sections(sections)
		self._corners = None
		self._horizontal = None
		grade = self.lines[0][0].grade
		if grade <= 0x04:
			self._grade = 1
		elif grade <= 0x06:
			self._grade = 2
		else:
			self._grade = 3

	@property
	def grade(self):
		return self._grade

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

	@property
	def corners(self):
		if not self._corners:
			self._corners = (self.top_left(), self.bottom_right())
		return self._corners

	def middle_point(self, horiz):
		longest = max(self.lines, key=lambda l: len(l))
		ltl = RoadSection.top_left(longest)
		lbr = RoadSection.bottom_right(longest)
		#tl_point, br_point = self.corners
		tl_point, br_point = ltl, lbr
		middle = Point(x=(tl_point.x + br_point.x) // 2,
					   y=(tl_point.y + br_point.y) // 2)
		if horiz:
			middle = Point(middle.x, lbr.y)
		else:
			middle = Point(lbr.x, middle.y)
		return middle

	def judge_horiz(self):
		tl_point, br_point = self.corners
		width = br_point.x - tl_point.x
		height = br_point.y - tl_point.y
		logging.debug("%s is %s", self.name, ('horizontal' if width > height else 'vertical'))
		return width > height

	@property
	def horizontal(self):
		if self._horizontal is None:
			self._horizontal = self.judge_horiz()
		return self._horizontal

	def head_point(self):
		if self.horizontal:
			self.lines = sorted(self.lines, key=lambda ln: ln[0].points[0].x)
			return self.lines[0][0].points[0]
		else:
			self.lines = sorted(self.lines, key=lambda ln: ln[0].points[0].y)
			return self.lines[0][0].points[0]

	def set_name_pos(self):
		middle = self.middle_point(self.horizontal)
		#head = self.head_point()
		logging.debug("%s horiz=%s", self.name, self.horizontal)
		for i, c in enumerate(self.name):
			pos = CharPosition(i, c, len(self.name))
			pos.set_pos(middle, self.horizontal)
			#pos.set_pos_head(head, self.horizontal)
			self.chars_pos.append(pos)

	def display_lines(self):
		dlines = []
		for ln in self.lines:
			points = reduce(lambda x,y: x + y[1:], [s.points for s in ln])
			dlines.append(points)
		return dlines

	@staticmethod
	def make_roads(grouped_sections):
		roads = {}
		for name in grouped_sections:
			roads[name] = Road(name, grouped_sections[name])
		return roads