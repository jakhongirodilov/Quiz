from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "opt1", "opt2", "opt3", "opt4", "answer"]