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
	next_ = _find_next(None, sections)
	while next_:
		sorted_sect.append(next_)
		next_ = _find_next(next_, sections)
	if not sections:
		return sorted_sect
	prev = _find_prev(sorted_sect[0], sections)
	while prev:
		sorted_sect.insert(0, prev)
		prev = _find_prev(prev, sections)
	return sorted_sect

def _find_next(current, sections):
	if not current:
		return sections.pop(0)
	for i,s in enumerate(sections):
		if s.points[0] == current.points[-1]:
			return sections.pop(i)
	return None

def _find_prev(current, sections):
	if not current:
		return sections.pop(0)
	for i,s in enumerate(sections):
		if s.points[-1] == current.points[0]:
			return sections.pop(i)
	return None

####

def _Lonlat2Pixel(lonlat, zoom=16):
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
		self.grade = int(sect.get('grade')[0:2], 16)
		self.direction = int(sect.get('direction'))
		self.points = [Point(float(xy[0]), float(xy[1])) for xy in sect.get('points')]

	def convert_points(self, zoom):
		self.points = [_Lonlat2Pixel(p, zoom) for p in self.points]
		#logging.debug(self.points)

	def points2pixels(self, mapinfo):
		def to_pixels(point):
			x = point.x - mapinfo.top_left.x
			y = point.y - mapinfo.top_left.y
			return Point(x, y)
		self.points = [to_pixels(p) for p in self.points]
		#logging.debug(self.points)

	@staticmethod
	def top_left(sections):
		points = reduce(lambda x,y: x+y, [s.points for s in sections])
		return top_left(points)

	@staticmethod
	def bottom_right(sections):
		points = reduce(lambda x,y: x+y, [s.points for s in sections])
		return bottom_right(points)

####

class RoadDataLoader():

	def __init__(self):
		self.data = {}

	def road_sections(self):
		all_sections = []
		grouped_sections = defaultdict(list)
		for id in self.data:
			sect = RoadSection(self.data[id])
			all_sections.append(sect)
			grouped_sections[sect.name].append(sect)
		for name in grouped_sections:
			logging.debug("%s has %d sections", name, len(grouped_sections[name]))
		return all_sections, grouped_sections

	def load_file(self, filename):
		with open(filename, encoding='utf-8') as f:
			for line in f:
				self.parse_line(line.strip())
		logging.debug("loaded %d records", len(self.data))

	def parse_line(self, line):
		entry = {}
		part1, part2 = line.split('&')
		entry['id'], entry['name'], entry['grade'], entry['direction'] = part1.split(',')
		entry['points'] = [tuple(xy.split(',')) for xy in part2.split(';') if xy]
		self.data[entry.get('id')] = entry
