import logging
import math
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

####

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

####

def convert_point(point, map_):
	p = Lonlat2Pixel(point)
	x = p.x - map_.top_left.x
	y = map_.height - abs(p.y - map_.top_left.y)
	return Point(x, y)

def Lonlat2Pixel(lonlat, zoom=16):
	longitude, latitude = lonlat[0], lonlat[1]
	_Num157 = 1.5707963267948966
	_Num57 = 57.295779513082323
	fd = 40075016.685578488 / ((1 << zoom) * 256)
	ia = (longitude / _Num57) * 6378137
	hT = - math.log(math.tan((_Num157 - latitude / _Num57) / 2)) * 6378137
	xPixel = round((ia + 20037508.342789244) / fd)
	yPixel = round((20037508.342789244 - hT) / fd)
	return Point(xPixel, yPixel)

####

class RoadSection():

	def __init__(self, sect):
		self.id = sect.get('id')
		self.name = sect.get('name')
		self.grade = sect.get('grade')
		self.direction = int(sect.get('direction'))
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
	def grouped_sections(road_data):
		all_sections = []
		road_sections = defaultdict(list)
		for id in road_data:
			sect = RoadSection(road_data[id])
			all_sections.append(sect)
			road_sections[sect.name].append(sect)
		for name in road_sections:
			logging.debug("%s has %d sections", name, len(road_sections[name]))
		return all_sections, road_sections