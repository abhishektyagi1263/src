from django import forms

class SearchForm(forms.Form):
    search_anime = forms.CharField( widget= forms.TextInput
                           (attrs={'class':'nav-search',
				  }))
