from django.db import models

# Create your models here.
class Speedtest(models.Model):
	public_ip = models.CharField(max_length=16)
	private_ip = models.CharField(max_length=16)
	latitude = models.FloatField()
	longitude = models.FloatField()
	is_wifi = models.BooleanField()
	wifi_ssid = models.CharField(max_length=50)
	wifi_strength = models.IntegerField()
	download = models.FloatField()
	upload = models.FloatField()
	imei = models.CharField(max_length=16)
	#time = models.CharField(max_length=50)
	year = models.IntegerField()
	month = models.IntegerField()
	date = models.IntegerField()
	hour = models.IntegerField()
	minute = models.IntegerField()
	second = models.IntegerField()

	carrier = models.CharField(max_length=16)
	signal_strength = models.IntegerField()
	network_type = models.IntegerField()
	network_strength = models.IntegerField()
	ping = models.FloatField()

	def __str__(self):
		return self.public_ip