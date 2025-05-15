from django import forms
from .models import note

class NoteForm(forms.ModelForm):
    class Meta:
        model=note
        fields=['title','content']