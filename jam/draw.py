import logging
from PIL import Image, ImageDraw, ImageFont, ImageColor

_COLORS = {1: (255, 0, 0), 2: (255, 255, 0), 3: (128, 255, 0),
		   4: (0, 255, 64), 5: (0, 255, 255), 6: (0, 128, 192),
		   7: (128, 128, 192), 8: (255, 0, 255), 9: (0, 0, 255)}

class DrawRoads():

	def __init__(self, roads, mapinfo):
		self.roads = roads
		self.mapinfo = mapinfo
		self.im = Image.new('RGB', (mapinfo.width, mapinfo.height))
		self.draw = ImageDraw.Draw(self.im)

	def draw_roads(self):
		logging.debug("drawing roads")
		line_width = {1: 10, 2: 5, 3: 3}
		for name in self.roads:
			W = line_width[self.roads[name].grade]
			for i,line in enumerate(self.roads[name].display_lines()):
				F = _COLORS.get(i+1, (192, 192, 192))
				self.draw.line(line, fill=F, width=W)

	def draw_names(self): 
		logging.debug("drawing road names")
		simsun_font = ImageFont.truetype("simsun.ttc", 24, encoding="unic")
		for name in self.roads:
			self.roads[name].set_name_pos()
			for cp in self.roads[name].chars_pos:
				#logging.debug("%s, %s", cp.pos, cp.char)
				self.draw.text(cp.pos, cp.char, font=simsun_font)

	def draw_and_save(self, filename):
		self.draw_roads()
		self.draw_names()
		self.im.save(filename, "PNG")
