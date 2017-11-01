from django.db import models
from django.utils import timezone
from django.urls import reverse


def image_path(instance, filename):
    return os.path.join('uploads/coins/', str(instance.some_identifier),'/', 'filename.ext')

# Create your models here.
class Coin(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('BD','Плохое')
	)

	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	country = models.CharField("Страна", max_length=128)
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
	
	
	def __str__(self):
		return self.value+' '+self.year
	def title(self):
		return str(self)
	def url(self):
		return ''+str(self.id)
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
	

 
