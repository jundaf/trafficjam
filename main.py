import sys
import os.path

import logging
logging.basicConfig(level=logging.DEBUG)

from jam.loader import RoadDataLoader
from jam.section import RoadSection, MapInfo
from jam.road import Road
from jam.draw import DrawRoads

ERROR = 1
ERROR_CMDLINE = 2

MAP_SIZE = 1000

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

	sections = RoadSection.make_sections(data_loader.road_data)
	roads = Road.parse_roads(sections)

	top_left = Road.top_left_corner(roads)
	bottom_right = Road.bottom_right_corner(roads)
	logging.debug("Top left    : %s", top_left)
	logging.debug("Bottom right: %s", bottom_right)

	mapinfo = MapInfo(top_left, bottom_right, MAP_SIZE)
	for name in roads:
		roads[name].convert_points(mapinfo)
		roads[name].set_name_pos()

	dr = DrawRoads(roads, MAP_SIZE)
	dr.draw_and_save(sys.argv[2])


if __name__ == '__main__':
	sys.exit(main())