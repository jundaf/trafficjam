import logging
from functools import reduce

from .section import *

CHAR_SIZE = 24

class CharPosition(object):

	def __init__(self, index, char, total):
		self.index = index
		self.char = char
		self.total = total
		self.pos = (0,0)

	def set_pos(self, middle, horiz):
		mid = self.total // 2 + 1
		x, y = middle.x, middle.y
		if horiz:
			x += (self.index - mid) * CHAR_SIZE
			y += 10
		else:
			x += 10
			y += (self.index - mid) * CHAR_SIZE
		self.pos = (x, y)


class Road():

	HIGHWAY, NORMAL, OTHER = 1, 2, 3

	def __init__(self, name, sections):
		self.name = name
		self._set_grade(sections[0])
		self.lines = []
		self.chars_pos = []
		self._parse_sections(sections)
		self._corners = None
		self._horizontal = None

	def _set_grade(self, section):
		grade = section.grade
		if grade <= 0x04:
			self.grade = Road.HIGHWAY
		elif grade <= 0x06:
			self.grade = Road.NORMAL
		else:
			self.grade = Road.OTHER

	def _parse_sections(self, sections):
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

	def _middle_point(self, horiz):
		longest = max(self.lines, key=lambda l: len(l))
		tl_point = RoadSection.top_left(longest)
		br_point = RoadSection.bottom_right(longest)
		middle = Point(x=(tl_point.x + br_point.x) // 2,
					   y=(tl_point.y + br_point.y) // 2)
		if horiz:
			return Point(middle.x, br_point.y)
		else:
			return Point(br_point.x, middle.y)

	def _judge_horiz(self):
		tl_point, br_point = self.corners
		width = br_point.x - tl_point.x
		height = br_point.y - tl_point.y
		logging.debug("%s is %s", self.name, ('horizontal' if width > height else 'vertical'))
		return width > height

	@property
	def horizontal(self):
		if self._horizontal is None:
			self._horizontal = self._judge_horiz()
		return self._horizontal

	def display_name(self):
		chars = []
		middle = self._middle_point(self.horizontal)
		for i, c in enumerate(self.name):
			char = CharPosition(i, c, len(self.name))
			char.set_pos(middle, self.horizontal)
			chars.append(char)
		return chars

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