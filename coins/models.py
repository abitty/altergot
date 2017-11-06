from django.db import models
from django.utils import timezone
from django.urls import reverse


def image_path(instance, filename):
    return os.path.join('uploads/coins/', str(instance.some_identifier),'/', 'filename.ext')

class Country(models.Model):
	country = models.CharField("Страна", max_length=128, blank=False)
	def __str__(self):
		return self.country
	def __unicode__(self):
		return self.country
	class Meta:
		verbose_name = "Страна"
		verbose_name_plural = "Страны"
	
	
# Create your models here.
class Coin(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('BD','Плохое')
	)

	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	#country = models.CharField('Страна',max_length=128, blank=True)
	country = models.ForeignKey(Country,on_delete=models.CASCADE)
	value = models.CharField("Номинал",max_length=128)
	year = models.CharField("Год на монете",max_length=4)
	specific = models.CharField("Особенности", max_length=255, blank=True)
	inuse = models.BooleanField("Хождение",default=False)
	haveit = models.BooleanField("В коллекции",default=True)
	condition = models.CharField("Состояние",
		max_length = 2,
		choices = COND_CHOICES,
		default = 'VG'
	)
	avers = models.ImageField("Аверс",upload_to = 'uploads/',blank=True)
	revers = models.ImageField("Реверс",upload_to = 'uploads/',blank=True)
	comment = models.CharField("Комментарии",max_length=255, blank=True)
	created_date = models.DateTimeField(
		default = timezone.now)
		
		
	last_country = None
	def set_lc(self, value):
		last_country = value
	def get_lc(self):
		return self.last_country
	
	class Meta:
		verbose_name = "Монета"
		verbose_name_plural = "Монеты"
	
	def __str__(self):
		return self.value+' '+self.year
	def title(self):
		return str(self)
	def url(self):
		return ''+str(self.id)+'?country='+str(self.country_id)
	def get_absolute_url(self):
		return reverse('list',kwargs={})
	def tags(self):
		return (self.value + \
		' ' + self.year + \
		' ' + self.country + \
		' ' + self.specific + \
		' ' + self.comment + \
		' ' + self.get_condition_display() + \
		' ' + {False:'нет',True:'есть'}[self.haveit]).lower()
	def condition_text(self):
		result = None
		for k,v in self.COND_CHOICES:
			if k == self.condition:
				result = v
		return result
		
		
from django.contrib import admin
admin.site.register(Country)		
		
		

 
