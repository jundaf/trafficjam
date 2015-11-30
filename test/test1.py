import pprint

ROAD_DATA2 = '''87382894,民族园路,0602,2&116.39176,39.98247;116.39186,39.98247;
87382895,民族园路,0602,2&116.39186,39.98247;116.39226,39.98248;
87382986,民族园路,0602,2&116.39158,39.98247;116.39176,39.98247;
87382985,民族园路,0602,2&116.39005,39.98243;116.39158,39.98247;
679613,民族园路,0602,2&116.38796,39.98241;116.38805,39.98241;
679641,民族园路,0602,2&116.39246,39.98249;116.39342,39.98252;
679644,民族园路,0602,2&116.39226,39.98248;116.39238,39.98248;
679645,民族园路,0602,2&116.39238,39.98248;116.39246,39.98249;
703698,民族园路,0602,2&116.38805,39.98241;116.38907,39.98243;
703700,民族园路,0602,2&116.38907,39.98243;116.39005,39.98243;
676575,民族园路,0602,2&116.39401,39.98253;116.39446,39.98254;
676574,民族园路,0602,2&116.39342,39.98252;116.39401,39.98253;'''

ROAD_DATA3 = '''87382988,民族园路,0602,3&116.39226,39.98265;116.39186,39.98263;
87382987,民族园路,0602,3&116.39186,39.98263;116.39176,39.98263;
679612,民族园路,0602,3&116.38805,39.98255;116.38796,39.98254;
679640,民族园路,0602,3&116.39341,39.98268;116.39245,39.98265;
679642,民族园路,0602,3&116.39238,39.98265;116.39226,39.98265;
679643,民族园路,0602,3&116.39245,39.98265;116.39238,39.98265;
703704,民族园路,0602,3&116.39005,39.98259;116.38907,39.98257;
703703,民族园路,0602,3&116.38907,39.98257;116.38805,39.98255;
676567,民族园路,0602,3&116.39445,39.9827;116.394,39.98269;
676566,民族园路,0602,3&116.394,39.98269;116.39341,39.98268;
38999006,民族园路,0602,3&116.39176,39.98263;116.39159,39.98263;
38999005,民族园路,0602,3&116.39159,39.98263;116.39005,39.98259;'''

def read_road_data(road_data):
	road_dict = {}
	for line in road_data.splitlines():
		entry = {}
		part1, part2 = line.split('&')
		entry['id'], entry['name'], entry['grade'], entry['direct'] = part1.split(',')
		entry['xyset'] = [tuple(xy.split(',')) for xy in part2.split(';') if xy]
		entry['xyset'] = [(float(xy[0]), float(xy[1])) for xy in entry['xyset']]
		#pprint.pprint(entry)
		road_dict[entry.get('id')] = entry
	#print("total: ", len(road_dict))
	return road_dict

def rect_length(xy1, xy2):
	l1 = xy2[0] - xy1[0]
	l2 = xy2[1] - xy1[1]
	return max(l1, l2) * 10 ** 6

def transform(xy, xy00, xymax):
	tt = (round((xy[0] - xy00[0]) * 10 ** 6),
		  round((xy[1] - xy00[1]) * 10 ** 6))
	return (tt[0] * 1000 // xymax, tt[1] * 1000 // xymax + 500)

def draw_and_save(*roads):
	from PIL import Image, ImageDraw
	im = Image.new('RGB',(1000,1000))
	draw = ImageDraw.Draw(im)
	for rd in roads:
		draw.line(rd, fill=128, width=5)
	del draw
	im.save("test.png", "PNG")

def road_lines(road_data):
	d = read_road_data(road_data)
	keys = sorted(d, key=lambda k: d[k].get('xyset')[0])
	pprint.pprint(keys)
	rect_len = rect_length(d[keys[0]].get('xyset')[0], d[keys[len(keys) - 1]].get('xyset')[1])
	#print(round(rect_len))
	lines = [d[key].get('xyset')[0] for key in keys]
	lines.append(d[keys[len(keys) - 1]].get('xyset')[1])
	lines = [transform(xy, d[keys[0]].get('xyset')[0], rect_len) for xy in lines]
	pprint.pprint(lines)
	return lines

####

if __name__ == '__main__':
	road1 = [(xy[0], xy[1] - 5) for xy in road_lines(ROAD_DATA2)]
	road2 = [(xy[0], xy[1] + 5) for xy in road_lines(ROAD_DATA3)]
	draw_and_save(road1, road2)
