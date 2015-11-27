import logging
from collections import defaultdict, namedtuple
from functools import reduce

Point = namedtuple('Point', ['x', 'y'])

def top_left(points):
	left = min([p.x for p in points])
	top = min([p.y for p in points])
	return Point(left, top)

def bottom_right(points):
	right = max([p.x for p in points])
	bottom = max([p.y for p in points])
	return Point(right, bottom)

def sorted_sections(sections):
	if not sections:
		return []
	elif len(sections) == 1:
		return [sections.pop(0)]
	sorted_sect = []
	next_ = find_next(None, sections)
	while next_:
		sorted_sect.append(next_)
		next_ = find_next(next_, sections)
	if not sections:
		return sorted_sect
	prev = find_prev(sorted_sect[0], sections)
	while prev:
		sorted_sect.insert(0, prev)
		prev = find_prev(prev, sections)
	return sorted_sect

def find_next(current, sections):
	if not current:
		return sections.pop(0)
	for i,s in enumerate(sections):
		if s.points[0] == current.points[-1]:
			return sections.pop(i)
	return None

def find_prev(current, sections):
	if not current:
		return sections.pop(0)
	for i,s in enumerate(sections):
		if s.points[-1] == current.points[0]:
			return sections.pop(i)
	return None


class MapInfo():

	def __init__(self, tl, br, ps):
		self.top_left = tl
		self.bottom_right = br
		self.pixel_size = ps
		self.width = int(round((br.x - tl.x) * 10 ** 6))
		self.height = int(round((br.y - tl.y) * 10 ** 6))
		logging.debug("%d, %d", self.width, self.height)


def convert_point(point, mapinfo):
	x = int(round((point.x - mapinfo.top_left.x) * 10 ** 6))
	y = int(round((point.y - mapinfo.top_left.y) * 10 ** 6))
	max_ = max(mapinfo.width, mapinfo.height)
	x = (x * mapinfo.pixel_size // max_)
	y = (y * mapinfo.pixel_size // max_)
	return Point(x, mapinfo.pixel_size - y)


class RoadSection():

	def __init__(self, sect):
		self.id = sect.get('id')
		self.name = sect.get('name')
		self.grade = sect.get('grade')
		self.direction = int(sect.get('direction'))
		#logging.debug(sect.get('points'))
		self.points = [Point(float(xy[0]), float(xy[1])) for xy in sect.get('points')]

	def convert_points(self, mapinfo):
		self.points = [convert_point(p, mapinfo) for p in self.points]
		#logging.debug(self.points)

	@staticmethod
	def top_left(sections):
		points = reduce(lambda x,y: x+y, [s.points for s in sections])
		return top_left(points)

	@staticmethod
	def bottom_right(sections):
		points = reduce(lambda x,y: x+y, [s.points for s in sections])
		return bottom_right(points)

	@staticmethod
	def make_sections(road_data):
		road_sections = defaultdict(list)
		for id in road_data:
			sect = RoadSection(road_data[id])
			road_sections[sect.name].append(sect)
		for name in road_sections:
			logging.debug("%s has %d sections", name, len(road_sections[name]))
		return road_sections