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
				'class': 'form-control'
			})
	class Meta(object):
		model = Coin
        #exclude = ('status',)
		fields = ['country','value','year','inuse','haveit','special','specific','specific','condition','avers','revers','comment']
		
		
class SearchForm(forms.ModelForm):
	country = ModelChoiceField(queryset=Country.objects, empty_label="Страна")
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
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
	
	def get(self, request):
		found_items= self.model.do_search(self.model,request)
		if found_items['sc']:
			#form = self.form_class(initial={'country':found_items['sc']})
			form = self.form_class(initial=request.GET)
		else:
			form = self.form_class()
		found_items['form'] = form
		return render(request, self.template_name, found_items)
	def get_last_country(self):
		return self.last_country


	
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
		qd = self.request.GET
		qd = self.model.get_last_query(self.model)
		lc = reverse('sel')+'?'+qd.urlencode(safe='/')
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
		qd = self.request.GET
		qd = self.model.get_last_query(self.model)
		lc = reverse('sel')+'?'+qd.urlencode(safe='/')
		return lc
	


	

