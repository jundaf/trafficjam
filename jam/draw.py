import logging
from PIL import Image, ImageDraw, ImageFont

class DrawRoads():

	def __init__(self, roads, wh):
		self.roads = roads
		self.im = Image.new('RGB', (wh[0], wh[1]))
		self.draw = ImageDraw.Draw(self.im)

	def draw_roads(self):
		logging.debug("drawing roads")
		for name in self.roads:
			for line in self.roads[name].display_lines():
				self.draw.line(line, fill=128, width=5)

	def draw_names(self):
		logging.debug("drawing road names")
		simsun_font = ImageFont.truetype("simsun.ttc", 24, encoding="unic")
		self.draw.text((0,0), "图吧", font=simsun_font)
		for name in self.roads:
			for cp in self.roads[name].chars_pos:
				#logging.debug("%s, %s", cp.pos, cp.char)
				self.draw.text(cp.pos, cp.char, font=simsun_font)

	def draw_and_save(self, filename):
		self.draw_roads()
		#self.draw_names()
		self.im.save(filename, "PNG")
