from .models import Coin, Country
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import re
from django.db.models import Q
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.forms import Textarea
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from django.forms import ModelChoiceField
from django.urls import reverse
from sets.models import Collection
import logging


logger = logging.getLogger(__name__)


# Create your views here.

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


class CoinForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CoinForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control',
				'style': 'width: auto;',
			})
	class Meta(object):
		model = Coin
        #exclude = ('status',)
		fields = ['country','value','year','inuse','haveit','special','sell','specific','condition','avers','revers','comment']
		
		
class SearchForm(forms.ModelForm):
	country = ModelChoiceField(queryset=Country.objects, empty_label="Страна")
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		#self.fields['colls'].queryset = Collection.coins_coll()
		
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
	class Meta(object):
		model = Coin
		fields = ['country']
		
class CoinDeleteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CoinForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
	class Meta(object):
		model = Coin
        #exclude = ('status',)
		fields = ['country','value','year']
		
# просмотр списка
class CoinsListView(ListView):
	model = Coin
	template_name = 'coin_list.html'
	form_class = SearchForm
	params = {}
	empty_request = True
	clear_search = False
	
	def request_or_session(self,request,key):
		exist = True
		try:
			s = self.params[key]
		except KeyError:
			exist = False
			s=''
		ss = request.session.get(key,'')
		request.session[key] = s
		if not exist:
			if self.empty_request and not self.clear_search:
				s = ss
			else:
				s = ''
		request.session[key] = s
		self.params[key]=s
		print ('key=',key,' req=',s,' ses=',ss)
		logger.debug('key:'+key+' rq='+s+' ss='+ss)
		
	def key_exist(self,request,key):
		exist = True
		try:
			s = self.params[key]
		except KeyError:
			exist = False
		return exist
		
	
	def get(self, request):
		self.params = request.GET.dict()
		print ("params=",self.params)
		logger.debug("request="+request.body.decode('utf-8'))
		self.clear_search = False
		self.request_or_session(request,'coll')
		if self.params.get('clr','0') == '1':
			self.clear_search = True
		if not self.key_exist(request,'country') and not self.key_exist(request,'v') and not self.key_exist(request,'y') and not self.key_exist(request,'q'):
			self.empty_request = True
		else:
			self.empty_request = False
		self.request_or_session(request,'country')
		self.request_or_session(request,'v')
		self.request_or_session(request,'y')
		self.request_or_session(request,'q')
		
		print ("params=",self.params)
		logger.debug(" clr="+str(self.clear_search)+" empty="+str(self.empty_request))
		
		found_items= self.model.do_search(self.model,self.params)
		if found_items['sc']:
			#form = self.form_class(initial={'country':found_items['sc']})
			form = self.form_class(initial=self.params)
		else:
			form = self.form_class()
			
			
		found_items['form'] = form
		collstr = self.params.get('coll','')
		found_items['coll'] = collstr
		if collstr:
			print ("collstr=",collstr)
			coll = Collection.objects.get(id=found_items['coll'])
			if coll:
				found_items['collection'] = coll			
				found_items['is_owner'] = coll.owner.id == request.user.id
		return render(request, self.template_name, found_items)


	
# просмотр записи
@method_decorator(login_required,'dispatch')
class CoinUpdate(UpdateView):
	model = Coin
	form_class = CoinForm
	template_name = 'coin_update.html'
	widgets = {
		'comment':Textarea(attrs={'cols':160, 'rows':40}),
	}
	def get_success_url(self):
		#qd = self.request.GET
		qd = self.model.get_last_query(self.model)
		if qd: 
			lc = reverse('sel')
			#lc = reverse('sel')+'?'+qd.urlencode(safe='/')
		else:
			lc = reverse('sel')
		return lc
		#return model.get_absolute_path()

@method_decorator(login_required,'dispatch')
class CoinCreate(CreateView):
	model = Coin
	form_class = CoinForm
	template_name = 'coin_update.html'

	def form_valid(self, form):
		# Мы используем ModelForm, а его метод save() возвращает инстанс
		# модели, связанный с формой. Аргумент commit=False говорит о том, что
		# записывать модель в базу рановато.
		try:
			form.instance = form.save(commit=False)
		except IntegrityError:
			print ("Form",form.as_p)

		# Теперь, когда у нас есть несохранённая модель, можно ей чего-нибудь
		# накрутить. Например, заполнить внешний ключ на auth.User. 
		form.instance.owner_id = self.request.user.id
		# А теперь можно сохранить в базу
		return super(CoinCreate, self).form_valid(form)

@method_decorator(login_required,'dispatch')
class CoinDelete(DeleteView):
	model = Coin
	form_class = CoinDeleteForm
	template_name = 'coin_delete.html'
	fields = ['coin_id','country','value','year']
	
	def get_success_url(self):
		qd = self.model.get_last_query(self.model)
		lc = reverse('sel')+'?'+qd.urlencode(safe='/')
		return lc
	


	

