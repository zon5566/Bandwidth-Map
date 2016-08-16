import json
import pymysql

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
minute = []

context = {'carrier': carrier, 'hour': hour}

def homepage(request):
	if request.method == 'POST':
		carrier_id = request.POST.get('carrier_select')
		hour = int(request.POST.get('hour_select'))
		
		print('View get:', carrier_id)
		print('Hour get:', hour)

		xcenter = float(request.POST.get('xcenter'))
		ycenter = float(request.POST.get('ycenter'))
		
		xblocksize = float(request.POST.get('xblocksize'))
		yblocksize = float(request.POST.get('yblocksize'))
		
		print('View get:', xcenter, ycenter, xblocksize, yblocksize)

		result = choose_block(xcenter, ycenter, xblocksize, yblocksize, 
			hour, carrier_id)

		for item in result:
			print(item[0], ':', '%d/%d/%d %d:%d %fBps'
				%(item[1],item[2],item[3],item[4],item[5],item[6]))
		print('Data amount:', len(result))

		render(request, 'testmap.html', context)
	return render(request, 'testmap.html', context)