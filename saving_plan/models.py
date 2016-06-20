from django.db import models


class Test(models.Model):
    mid = models.CharField(max_length = 20, primary_key = True)
    street_name = models.CharField(max_length = 20)
    block = models.CharField(max_length = 5)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
	    return self.mid
