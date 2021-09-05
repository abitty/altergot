from django.db import models
from django.utils.http import urlencode
from django.urls import reverse

# Create your models here.
class Collection(models.Model):
	COLLECTION_CHOICES =  (
		('CN','Монеты'),
		('BN','Купюры'),
	)
	owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	kind = models.CharField("Тип", default = 'CN', max_length = 2,choices = COLLECTION_CHOICES, blank=False)
	name = models.CharField("Название", max_length = 128, blank=False)
	public = models.BooleanField("Показывать",default=True)
	
	def __str__(self):
		return self.name
		
	def coll_by_kind(self,akind):
		obj = Collection.objects.filter(kind=akind, public=True).order_by('name') # was Collection.objects.filter
		return obj
		
	def url(self):
		if self.kind == 'CN':
			lq = {}
			lq['coll'] = self.id
			lc = reverse('sel')+'?'+urlencode(lq)+'&clr=1'
			#lc = '?'+urlencode(lq)
			print ("lc=",lc)
		elif self.kind == 'BN':
			lq = {}
			lq['coll'] = self.id
			#lc = '?'+urlencode(lq)+'&clr=1'
			lc = reverse('bsel')+'?'+urlencode(lq)+'&clr=1'
			print ("lc=",lc)
		return lc
		
	def coins_coll(self):
		return self.coll_by_kind(self,'CN')
		
	def bones_coll(self):
		return self.coll_by_kind(self,'BN')
		
	class Meta:
		verbose_name = "Коллекция"
		verbose_name_plural = "Коллекции"
	

