import pymysql

'''
one block = 200 meters * 200 meters
East - West : [121.45278: 0.001966: 121.65833] -> 104(.55) blocks
South - North : [24.95608: 0.001802: 25.21218] -> 142(.12) blocks

'''
XORIGIN = 121.45278
YORIGIN = 24.95608
XBLOCK_SIZE = 0.001966/2
YBLOCK_SIZE = 0.001802/2

#connect to mySQL
db = pymysql.connect(host='127.0.0.1', user='b02505006', passwd='f129365102', db='map')
cursor = db.cursor();

def choose_block(xcenter, ycenter, xblock, yblock, hour, carrier):
	xstart = xcenter - xblock/2;
	xend = xcenter + xblock/2;
	ystart = ycenter - yblock/2;
	yend = ycenter + yblock/2;

	inst = '''select id, year, month, date, hour, minute, download
		from speedtest where
		longitude > %f and longitude < %f
		and latitude > %f and latitude < %f
		and hour = %d''' %(xstart, xend, ystart, yend, hour)
	if(not carrier==''):
		inst = inst + ' and carrier = %s'%(carrier)
	#execute mySQL
	cursor.execute(inst)

	result = cursor.fetchall()
	return result;