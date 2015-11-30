import math

POINT = (116.37782,39.98862)
P2 = (116.39446,39.98254)

_Num157 = 1.5707963267948966
_Num57 = 57.295779513082323

def Lonlat2Pixel(ll, zoom=1):
	longitude, latitude = ll
	fd = 40075016.685578488 / ((1 << zoom) * 256)
	ia = (longitude / _Num57) * 6378137
	hT = - math.log(math.tan((_Num157 - latitude / _Num57) / 2)) * 6378137
	print(fd, ia, hT)
	xPixel = round((ia + 20037508.342789244) / fd, 10)
	yPixel = round((20037508.342789244 - hT) / fd, 10)
	return xPixel, yPixel

def main():
	print(Lonlat2Pixel(POINT, 20))
	print(Lonlat2Pixel(P2, 20))

if __name__ == '__main__':
	main()