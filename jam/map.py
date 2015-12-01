import logging
from .section import Lonlat2Pixel

class RoadMap(object):

	def __init__(self, top_left, bottom_right, zoom):
		self._zoom_level = zoom
		self.top_left = Lonlat2Pixel(top_left, zoom)
		self.bottom_right = Lonlat2Pixel(bottom_right, zoom)
		self.width = self.bottom_right.x - self.top_left.x
		self.height = abs(self.bottom_right.y - self.top_left.y)
		logging.debug("width={}, height={}".format(self.width, self.height))

	def zoom_level():
		doc = "The zoom_level property."
		def fget(self):
			return self._zoom_level
		def fset(self, value):
			self._zoom_level = value
		def fdel(self):
			del self._zoom_level
		return locals()
	zoom_level = property(**zoom_level())