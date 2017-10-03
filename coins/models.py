from django.db import models
from django.utils import timezone

# Create your models here.
class Coin(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('BD','Плохое')
	)
	owner = models.ForeignKey('auth.User')
	country = models.CharField(max_length=128)
	value = models.CharField(max_length=128)
	year = models.CharField(max_length=4)
	specific = models.CharField(max_length=255)
	inuse = models.BooleanField(default=False)
	haveit = models.BooleanField(default=True)
	condition = models.CharField(
		max_length = 2,
		choices = COND_CHOICES,
		default = 'VG'
	)
	avers = models.ImageField(upload_to = 'uploads/')
	revers = models.ImageField(upload_to = 'uploads/')
	comment = models.CharField(max_length=255)
	created_date = models.DateTimeField(
		default = timezone.now)
	
	def __str__(self):
		return self.value+' '+self.year




