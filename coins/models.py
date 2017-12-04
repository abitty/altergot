from django.db import models
from django.utils import timezone
from django.urls import reverse
from sets.models import Collection
import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import re


#logger = logging.getlogger(coins.models)
logger = logging.getLogger(__name__)

#def image_path(instance, filename):
#    return os.path.join('uploads/coins/', str(instance.some_identifier),'/', 'filename.ext')



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


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
		
	
def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]	
	
	
# Create your models here.
class Coin(models.Model):
	COND_CHOICES = (
		('MN','Отличное'),
		('VG','Хорошее'),
		('MD', 'Среднее'),
		('BD','Плохое')
	)

	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE, verbose_name="Владелец")
	country = models.ForeignKey(Country,on_delete=models.CASCADE, verbose_name="Страна")
	value = models.CharField("Номинал",max_length=128)
	year = models.CharField("Год на монете",max_length=64, blank=True)
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
		verbose_name = "Монета"
		verbose_name_plural = "Монеты"
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
	def thumb_size(self):
		if self.small:
			return "80x80"
		else:
			return "120x120"
	def expand_query(self, query):
		print ("orig",query)
		nq = normalize_query(query)
		print ("norm",nq)
		pfx = '';
		res = ''
		for q in nq:
			res = pfx.join([res,"`comment` LIKE '%%{0}%%' OR `specific` LIKE '%%{0}%%'".format(q)])
			pfx = ' OR '
		if res:
			res = "({})".format(res)
		return res
		
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
	
		sv = request.get('v','')
		if sv:
			where = prefix.join([where,"`value` LIKE '"+sv+"%%'"])
			empty_request = False
			prefix = ' AND '
		
		sq = request.get('q','')
		if sq:
			where  = prefix.join([where,self.expand_query(self,sq)])
			#where = prefix.join([where,"(`comment` LIKE '%%"+sq+"%%' OR `specific` LIKE '%%"+sq+"%%')"])
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
		if coll:
			where = prefix.join([where, '`owner_id`='+str(coll.owner_id)])
			sql_str = "SELECT * FROM `coins_coin`"
			if where:
				sql_str += where 
			if not empty_request:
				sql_str += ' ORDER BY `year`,`value`'
				print ("SQL:",sql_str)
				logger.debug("SQL: "+sql_str)
				found_items = Coin.objects.raw(sql_str)
				
		return {'sc':sc, 'y': sy, 'v':sv, 'q': sq, 'object_list': found_items,'after_search': not empty_request}
		
			
		
		
		
from django.contrib import admin
admin.site.register(Country)		
		
		

 
