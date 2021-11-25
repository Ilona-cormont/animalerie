from django import forms
from .models import Animal
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Animal
        fields = ('lieu',)


class AddForm(forms.ModelForm): 
  
    class Meta: 
        model = Animal 
        fields = ('id_animal', 'etat', 'type', 'race', 'photo', 'lieu',) 
