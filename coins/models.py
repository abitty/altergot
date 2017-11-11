from django.db import models
from django.utils import timezone
from django.urls import reverse
from sets.models import Collection


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
		indexes = [
			models.Index(fields=['country']),
		]
		
	
	
# Create your models here.
class Coin(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('MD', 'Среднее'),
		('BD','Плохое')
	)

	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	country = models.ForeignKey(Country,on_delete=models.CASCADE)
	value = models.CharField("Номинал",max_length=128)
	year = models.CharField("Год на монете",max_length=64, blank=True)
	specific = models.CharField("Особенности", max_length=255, blank=True)
	inuse = models.BooleanField("Хождение",default=False)
	haveit = models.BooleanField("В коллекции",default=True)
	special = models.BooleanField("Памятная",default=False)
	sell = models.BooleanField("Продажа/обмен",default=False, blank=True)
	condition = models.CharField("Состояние", default = 'VG', max_length = 2,choices = COND_CHOICES)
	avers = models.ImageField("Аверс",upload_to = 'uploads/',blank=True)
	revers = models.ImageField("Реверс",upload_to = 'uploads/',blank=True)
	comment = models.CharField("Комментарии",max_length=255, blank=True)
	created_date = models.DateTimeField(
		default = timezone.now)
		
		
	last_query = {}
	class Meta:
		verbose_name = "Монета"
		verbose_name_plural = "Монеты"
		indexes = [
			models.Index(fields=['year', 'value']),
		]
	
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
	def set_last_query(self, lq):
		self.last_query = list(lq)
	def get_last_query(self):
		return self.last_query 
		
	def do_search(self,request):
		self.set_last_query(self,request)
		found_items = None
		where = '' 
		empty_request = True
		sy = '';
		prefix = ' WHERE '
			
		sy = request.get('y','')
		if sy:
			where = prefix.join([where,"`year` LIKE '"+sy+"%%'"])
			empty_request = False
			prefix = ' AND '
	
		sv = request.get('v','');
		if sv:
			where = prefix.join([where,"`value` LIKE '"+sv+"%%'"])
			empty_request = False
			prefix = ' AND '
		
		sq = request.get('q','');
		if sq:
			where = prefix.join([where,"(`comment` LIKE '%%"+sq+"%%' OR `specific` LIKE '%%"+sq+"%%')"])
			empty_request = False
			prefix = ' AND '
			
		s = request.get('h','')
		if s:
			where = prefix.join([where, '`haveit`='+s])
			empty_request = False
			prefix = ' AND '
			
		sc = request.get('country','')
		if sc:
			where = prefix.join([where, '`country_id`='+sc])
			empty_request = False
			prefix = ' AND '
			
		coll = None	
		cs = request.get('coll','')
		if cs.isdigit():
			coll = Collection.objects.get(id=cs)
		print ("cs=",cs, " isdigit:",cs.isdigit(), " coll=",coll)
		if coll:
			where = prefix.join([where, '`owner_id`='+str(coll.owner_id)])
			sql_str = "SELECT * FROM `coins_coin`"
			if where:
				sql_str += where 
			if not empty_request:
				sql_str += ' ORDER BY `year`,`value`'
				print ("SQL:",sql_str)
				found_items = Coin.objects.raw(sql_str)
		return {'sc':sc, 'y': sy, 'v':sv, 'q': sq, 'object_list': found_items,'after_search': not empty_request}
		
			
		
		
		
from django.contrib import admin
admin.site.register(Country)		
		
		

 
