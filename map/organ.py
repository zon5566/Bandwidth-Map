import csv
import re
import sys

with open ('static/test_result2.csv', 'w', newline="") as wfile, open ('static/test_result.csv',encoding='cp950') as rfile:
	fieldnames = ['PUBLIC_IP', 'PRIVATE_IP', 'LAT', 'LON', 'IS_WIFI',
			'WIFI_STRENGTH', 'DOWNLOAD', 'UPLOAD',
			'IMEI', 'YEAR', 'MONTH', 'DATE', 'HOUR', 'MINUTE', 
			'CARRIER', 'SIGNAL_STRENGTH', 'NETWORK_TYPE',
			'NETWORK_STRENGTH', 'PING']
	writer = csv.DictWriter(wfile, fieldnames=fieldnames)
	writer.writeheader()

	reader = csv.DictReader(rfile)		
	i = 0;
	for row in reader:
		if float(row['LAT'])<=0 or float(row['LON'])<=0:
			continue
	
		if row['NETWORK_STRENGTH'] == str(0):
			continue

	#	if re.match('466',row['CARRIER'])==None:
	#		continue

	#	row['WIFI_SSID'] = row['WIFI_SSID'].replace('"','').strip()
		try:
			time_s = row['TIME'].split()
			time_former = time_s[0].split('/')
			time_latter = time_s[1].split(':')
		except:
			i = i+1
			print('error:', i, 'at ID:', row['ID'])
			print(sys.exc_info()[0])
			continue
	#	print(time_former[0], time_former[1], time_former[2], time_latter[0], time_latter[1])
		writer.writerow({
			'PUBLIC_IP': row['PUBLIC_IP'],
			'PRIVATE_IP': row['PRIVATE_IP'],
			'LAT': row['LAT'],
			'LON': row['LON'],
			'IS_WIFI': row['IS_WIFI'],
	#		'WIFI_SSID': row['WIFI_SSID'],
			'WIFI_STRENGTH': row['WIFI_STRENGTH'],
			'DOWNLOAD': row['DOWNLOAD'],
			'UPLOAD': row['UPLOAD'],
			'IMEI': row['IMEI_CODE'],
			'YEAR': time_former[0],
			'MONTH': time_former[1],
			'DATE': time_former[2],
			'HOUR': time_latter[0],
			'MINUTE': time_latter[1],
			'CARRIER': row['CARRIER'],
			'SIGNAL_STRENGTH': row['SIGNAL_STRENGTH'],
			'NETWORK_TYPE': row['NETWORK_TYPE'],
			'NETWORK_STRENGTH': row['NETWORK_STRENGTH'],
			'PING': row['PING']
			})