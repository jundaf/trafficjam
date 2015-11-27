import logging

class RoadDataLoader():

	def __init__(self):
		self.data = {}

	@property
	def road_data(self):
		return self.data

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
