from django import forms

class SearchForm(forms.Form):
    search_anime = forms.CharField( initial='Search Anime', label="", widget= forms.TextInput
                           (attrs={'class':'nav-search',
				  }))
