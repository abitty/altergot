from django.db import models
from django.utils import timezone
from django.urls import reverse
from sets.models import Collection
from coins.models import Country
import logging


logger = logging.getLogger(__name__)

# Create your models here.
class Bone(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('MD', 'Среднее'),
		('BD','Плохое')
	)

	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE, verbose_name="Владелец")
	country = models.ForeignKey(Country,on_delete=models.CASCADE, verbose_name="Страна")
	value = models.CharField("Номинал",max_length=128)
	year = models.CharField("Год на купюре",max_length=64, blank=True)
	specific = models.CharField("Особенности", max_length=255, blank=True)
	inuse = models.BooleanField("Хождение",default=False)
	haveit = models.BooleanField("В коллекции",default=True)
	special = models.BooleanField("Памятная",default=False)
	sell = models.BooleanField("Продажа/обмен",default=False, blank=True)
	condition = models.CharField("Состояние", default = 'VG', max_length = 2,choices = COND_CHOICES, blank=True)
	avers = models.ImageField("Аверс",upload_to = 'uploads/',blank=True)
	revers = models.ImageField("Реверс",upload_to = 'uploads/',blank=True)
	small = models.BooleanField("Маленькая",default=False)
	comment = models.CharField("Комментарии",max_length=255, blank=True)
	created_date = models.DateTimeField(
		default = timezone.now)
		
		
	class Meta:
		verbose_name = "Купюра"
		verbose_name_plural = "Купюры"
		indexes = [
			models.Index(fields=['year', 'value']),
		]
	
	def __str__(self):
		return self.value+' '+self.year
	def url(self):
		return ''+str(self.id)
	def title(self):
		return self.__str__()
	def get_absolute_url(self):
		return reverse('list',kwargs={})
	def condition_text(self):
		result = None
		for k,v in self.COND_CHOICES:
			if k == self.condition:
				result = v
		return result
	def landscape(self):
		res = True
		if self.avers and self.avers.width < self.avers.height:
			res = False
		if self.revers and self.revers.width < self.revers.height:
			res = False
		return res
	def thumb_size(self):
		if self.landscape():
			if self.small:
				return "180"
			else:
				return "280"
		else:
			if self.small:
				return "120"
			else:
				return "180"
	def do_search(self,request):
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
			if s == '2':
				where = prefix.join([where, "`sell`=true"]) # поиск монет "на продажу", которых больше одной
			else:
				where = prefix.join([where, '`haveit`='+s]) # поиск в коллекции/в хотелках
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
			sql_str = "SELECT * FROM `bones_bone`"
			if where:
				sql_str += where 
			if not empty_request:
				sql_str += ' ORDER BY `year`,`value`'
				print ("SQL:",sql_str)
				logger.debug("SQL: "+sql_str)
				found_items = Bone.objects.raw(sql_str)
				
		return {'sc':sc, 'y': sy, 'v':sv, 'q': sq, 'object_list': found_items,'after_search': not empty_request}
		
