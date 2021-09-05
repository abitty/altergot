from django.shortcuts import render
from sets.models import Collection
from django import forms
from django.forms import ModelChoiceField

# Create your views here.

class SearchForm(forms.ModelForm):
	#name = ModelChoiceField(queryset=Collection.coins_coll(self), empty_label=None)
	name = ModelChoiceField(queryset= Collection.objects.filter(kind='CN', public=True).order_by('name'))
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
	class Meta(object):
		model = Collection
		fields = ['name']


def index(request):
	model = Collection
	coins_coll = model.coins_coll(model)
	bones_coll = model.bones_coll(model)
	return render(request,'index.html',{'coins_coll': coins_coll,'bones_coll': bones_coll})
