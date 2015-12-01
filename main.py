import sys
import os.path

import logging
logging.basicConfig(level=logging.DEBUG)

from jam.loader import RoadDataLoader
from jam.section import RoadSection
from jam.road import Road
from jam.draw import DrawRoads
from jam.map import RoadMap

ERROR = 1
ERROR_CMDLINE = 2


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

	all_sections, grouped_sections = RoadSection.grouped_sections(data_loader.road_sections)
	roads = Road.make_roads(grouped_sections)

	top_left = RoadSection.top_left(all_sections)
	bottom_right = RoadSection.bottom_right(all_sections)
	logging.debug("Top left    : %s", top_left)
	logging.debug("Bottom right: %s", bottom_right)

	road_map = RoadMap(top_left, bottom_right, zoom=16)
	for sect in all_sections:
		sect.convert_points(road_map)

	# for name in roads:
	# 	roads[name].judge_horiz()
	dr = DrawRoads(roads, road_map)
	dr.draw_and_save(sys.argv[2])


if __name__ == '__main__':
	sys.exit(main())