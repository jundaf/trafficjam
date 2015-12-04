import sys
import os.path

import logging
logging.basicConfig(level=logging.DEBUG)

from jam.section import RoadSection, RoadDataLoader
from jam.road import Road
from jam.draw import DrawRoads


ERROR = 1
ERROR_CMDLINE = 2


class MapGeometry(object):

	def __init__(self, top_left, bottom_right):
		self.top_left = top_left
		self.bottom_right = bottom_right
		logging.debug("Top left    : %s", top_left)
		logging.debug("Bottom right: %s", bottom_right)

	@property
	def width(self):
		return self.bottom_right.x - self.top_left.x

	@property
	def height(self):
		return abs(self.bottom_right.y - self.top_left.y)


def main():
	if len(sys.argv) < 3:
		print("Usage: {} data_file out_file".format(sys.argv[0]), file=sys.stderr)
		return ERROR_CMDLINE
	if not os.path.exists(sys.argv[1]):
		logging.error("file not found: %s", sys.argv[1])
		return ERROR

	logging.debug("input file: %s", sys.argv[1])
	logging.debug("output file: %s", sys.argv[2])

	data_loader = RoadDataLoader()
	data_loader.load_file(sys.argv[1])

	all_sections, grouped_sections = data_loader.road_sections()
	roads = Road.make_roads(grouped_sections)
	for sect in all_sections:
		sect.convert_points(zoom=16)

	top_left = RoadSection.top_left(all_sections)
	bottom_right = RoadSection.bottom_right(all_sections)

	mapinfo = MapGeometry(top_left, bottom_right)
	logging.debug("width={}, height={}".format(mapinfo.width, mapinfo.height))
	for sect in all_sections:
		sect.points2pixels(mapinfo)

	dr = DrawRoads(roads, mapinfo)
	dr.draw_and_save(sys.argv[2])


if __name__ == '__main__':
	sys.exit(main())