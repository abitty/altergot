from .models import Coin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import re
from django.db.models import Q
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.forms import Textarea
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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



def filtered(request):


	found_items = None
	where = '' 
	s = ''
	if ('y' in request.GET):
		sy = request.GET['y']
	if sy:
		where = "`year` LIKE '"+sy+"%%'"
	
	sv = '';
	if 'v' in request.GET:
		sv = request.GET['v']
	if sv:
		if where:
			where = ' AND '.join([where,"`value` LIKE '"+sv+"%%'"])
		else:
			where = "`value` LIKE '"+sv+"%%'"
	sq = ''
	if 'q' in request.GET:
		sq = request.GET['q']
	if sq:
		if where:
			where = ' AND '.join([where,"(`comment` LIKE '%%"+sq+"%%' OR `specific` LIKE '%%"+sq+"%%')"])
		else:
			where = "(`comment` LIKE '%%"+sq+"%%' OR `specific` LIKE '%%"+sq+"%%')"
	s = ''
	if 'h' in request.GET:
		s = request.GET['h']
	if s:
		if where:
			where = ' AND '.join([where, '`haveit`='+s])
		else:
			where = '`haveit`='+s
	sql_str = "SELECT * FROM `coins_coin`"
	if where:
		sql_str += " WHERE "+where 
	found_items = Coin.objects.raw(sql_str)
	
	return render(request,'coin_filtered.html',
	{'sy': sy, 'sv':sv, 'sq': sq, 'object_list': found_items,'after_search': 'True'})



# просмотр списка
class CoinsListView(ListView):
	model = Coin
	template_name = 'coin_filtered.html'



from django import forms

class CoinForm(forms.ModelForm):
	class Meta(object):
		model = Coin
        #exclude = ('status',)
		fields = ['country','value','year','specific','inuse','haveit','condition','avers','revers','comment']
	
# просмотр записи
@method_decorator(login_required,'dispatch')
class CoinUpdate(UpdateView):
	model = Coin
	form_class = CoinForm
	#fields = ['country','value','year','specific','inuse','haveit','condition','avers','revers','comment']
	template_name = 'coin_update.html'
	widgets = {
		'comment':Textarea(attrs={'cols':160, 'rows':40}),
	}


	
def get_success_url(self):
	return model.get_absolute_path()

@method_decorator(login_required,'dispatch')
class CoinCreate(CreateView):
	model = Coin
	#exclude = ['owner']
	form_class = CoinForm
	#fields = ['country','value','year','specific','inuse','haveit','condition','avers','revers','comment','created_date']
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
		# накрутить. Например, заполнить внешний ключ на auth.User. У нас же
		# блог, а не анонимный имижборд, правда?
		form.instance.owner_id = self.request.user.id
		print ("owner_id=",form.instance.owner_id)	
		# А теперь можно сохранить в базу
		#instance.save() 
		return super(CoinCreate, self).form_valid(form)

		#return redirect(self.get_success_url())


