import json
import pymysql

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from django.shortcuts import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings

from .models import Speedtest

from .getblock import choose_block

carrier= [	{'id': 46601, 'name':'遠傳電信'}, 
			{'id': 46692, 'name':'中華電信'},
			{'id': 46697, 'name':'台灣大哥大'},
			{'id': 46689, 'name':'威寶電信'},
			{'id': 46605, 'name':'亞太電信'},]

hour = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
minute = [	{'id': 0, 'name':'0~9'},
			{'id': 1, 'name':'10~19'},
			{'id': 2, 'name':'20~29'},
			{'id': 3, 'name':'30~39'},
			{'id': 4, 'name':'40~49'},
			{'id': 5, 'name':'50~59'},]

context = {'carrier': carrier, 'hour': hour, 'minute': minute}

def homepage(request):
	if request.method == 'POST':
		carrier_id = request.POST.get('carrier_select')
		hour = int(request.POST.get('hour_select'))
		minute = int(request.POST.get('minute_select'))

		xcenter = float(request.POST.get('xcenter'))
		ycenter = float(request.POST.get('ycenter'))
		
		xblocksize = float(request.POST.get('xblocksize'))
		yblocksize = float(request.POST.get('yblocksize'))
		
		result = choose_block(xcenter, ycenter, xblocksize, yblocksize, 
			hour, minute, carrier_id)

		hist_list = list()
		for item in result:
			print('%d/%d/%d %d:%d'%(item[0],item[1],item[2],item[3],item[4]))
			hist_list.append(item[5])

		print('Data amount:', len(result))

		ax = plt.gca()
		ax.yaxis.set_major_locator(MaxNLocator(integer=True))

		hist, bins = np.histogram(hist_list, range(0,15000,100))
#		hist, bins = np.histogram(hist_list, range(int(min(hist_list))-100,int(max(hist_list))+100,100))
		print(int(min(hist_list)), int(max(hist_list)))
		center = (bins[:-1] + bins[1:]) / 2
		plt.bar(center, hist, align='center', width=100)

		set_attribute(plt, hour, minute, carrier_id, hist_list)

		plt.show()
		plt.close()

		render(request, 'testmap.html', context)
	return render(request, 'testmap.html', context)


def set_attribute(plt, hour, minute, carrier, hist_list):
	plt.xlabel('Download bandwidth (KBytes)')
	print(min(hist_list), max(hist_list))
	#plt.xticks(np.arange(int(min(hist_list)), int(max(hist_list)), 300))
	plt.ylabel('Number of sample')
	plt.ylim(ymin=0)
	if carrier != '':
		plt.title('%d:%d (last 10 minutes) carrier=%s \nDistribution Plot'%(hour, minute*10, carrier))

	else:
		plt.title('%d:%d (last 10 minutes) \nDistribution Plot'%(hour, minute*10))