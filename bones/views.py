from coins.models import Country
from bones.models import Bone
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

class BoneForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BoneForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control',
				'style': 'width: auto;',
			})
	class Meta(object):
		model = Bone
		fields = ['country','value','year','inuse','haveit','special','sell','specific','condition','avers','revers','small','comment']
		
		
class BoneSearchForm(forms.ModelForm):
	country = ModelChoiceField(queryset=Country.objects, empty_label="Страна")
	def __init__(self, *args, **kwargs):
		super(BoneSearchForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
	class Meta(object):
		model = Bone
		fields = ['country']
		
class BoneDeleteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BoneForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
	class Meta(object):
		model = Bone
		fields = ['country','value','year']
		
# просмотр списка
class BonesListView(ListView):
	model = Bone
	template_name = 'bone_list.html'
	form_class = BoneSearchForm
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
			
		show_country = False	
		if not self.params.get('country',''):
			show_country = True	
		self.request_or_session(request,'country')
		self.request_or_session(request,'v')
		self.request_or_session(request,'y')
		self.request_or_session(request,'q')
		
		print ("params=",self.params," show_country=",show_country)
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
			coll = Collection.objects.get(id=found_items['coll'])
			if coll:
				found_items['collection'] = coll			
				found_items['is_owner'] = coll.owner.id == request.user.id
				found_items['show_country'] = show_country
		return render(request, self.template_name, found_items)


	
# просмотр записи
@method_decorator(login_required,'dispatch')
class BoneUpdate(UpdateView):
	model = Bone
	form_class = BoneForm
	template_name = 'bone_update.html'
	widgets = {
		'comment':Textarea(attrs={'cols':160, 'rows':40}),
	}
	def get_success_url(self):
		lc = reverse('bsel')
		return lc

@method_decorator(login_required,'dispatch')
class BoneCreate(CreateView):
	model = Bone
	form_class = BoneForm
	template_name = 'bone_update.html'

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
		return super(BoneCreate, self).form_valid(form)
	def get_success_url(self):
		lc = reverse('bsel')
		return lc

@method_decorator(login_required,'dispatch')
class BoneDelete(DeleteView):
	model = Bone
	form_class = BoneDeleteForm
	template_name = 'bone_delete.html'
	fields = ['bone_id','country','value','year']
	
	def get_success_url(self):
		lc = reverse('bsel')
		return lc
	


	

