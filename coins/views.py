from .models import Coin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import re
from django.db.models import Q
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.forms import Textarea

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

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects. 
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query 
    return query


def filtered(request):

	query_string = ''
	found_items = None
	if ('q' in request.GET) and request.GET['q'].strip():
		
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['value', 'year', 'country', 'specific', 'comment'])
		found_items = Coin.objects.filter(entry_query)

	return render(request,'coins/coin_filtered.html',
	{'query_string': query_string, 'found_items': found_items})



# просмотр списка
class CoinsListView(ListView):
	model = Coin

	
# просмотр записи
class CoinUpdate(UpdateView):
	model = Coin
	fields = ['country','value','year','specific','inuse','haveit','condition','avers','revers','comment']
	template_name = 'coins/coin_update.html'
	widgets = {
		'comment':Textarea(attrs={'cols':160, 'rows':40}),
	}
	
def get_success_url(self):
	return model.get_absolute_path()

class CoinCreate(CreateView):
	model = Coin
	exclude = ['owner']
	#fields = ['country','value','year','specific','inuse','haveit','condition','avers','revers','comment','created']
	template_name = 'coins/coin_update.html'
	
