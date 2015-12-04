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
		self._parse_sections(sections)
		self._corners = None
		self._horizontal = None
		self._name_line = []

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
		name_line = (self._name_line if self._name_line else longest)
		tl_point = RoadSection.top_left(name_line)
		br_point = RoadSection.bottom_right(name_line)
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

	def normalize_lines(self, lines):
		tmp_lines = []
		for l in lines:
			p1 = l[0].points[0]
			p2 = l[-1].points[-1]
			if self.horizontal:
				if p1.x > p1.x:
					tmp_lines.append(list(reversed(l)))
				else:
					tmp_lines.append(l)
			else:
				if p1.y > p1.y:
					tmp_lines.append(list(reversed(l)))
				else:
					tmp_lines.append(l)
		return tmp_lines

	def _shift_lines(self):
		if len(self.lines) == 1 or len(self.lines) > 4:
			return
		lines = [l for l in self.lines if (len(l) > 3 and any_two_or_three(l))]
		if len(lines) not in (2, 4):
			return

		def x_or_y(line):
			if self.horizontal:
				return line[0].points[0].x
			else:
				return line[0].points[0].y

		lines = self.normalize_lines(lines)
		lines = sorted(lines, key=x_or_y)
		while lines:
			self._shift_line_pair(*lines[:2])
			lines = lines[2:]

	def _shift_line_pair(self, la, lb):
		if self.horizontal:
			ya = [la[0].points[0].y, la[-1].points[-1].y]
			yb = [lb[0].points[0].y, lb[-1].points[-1].y]
			if ya > yb:
				la, lb = lb, la
			shift_lines_vertical(la, lb)
		else:
			xa = [la[0].points[0].x, la[-1].points[-1].x]
			xb = [lb[0].points[0].x, lb[-1].points[-1].x]
			if xa > xb:
				la, lb = lb, la
			shift_lines_horizontal(la, lb)
		self._name_line = max(self._name_line, lb, key=lambda l: len(l))

	def display_lines(self):
		self._shift_lines()
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