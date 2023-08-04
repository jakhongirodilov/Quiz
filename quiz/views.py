from typing import Any, Dict
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from .models import Subject, Question, Result
from .forms import QuestionForm


def home(request):
    subjects = Subject.objects.all()
    context = {
        'subjects':subjects
    }

    return render(request, 'home.html', context)


@login_required
def subject(request, pk): 
    subject = Subject.objects.get(id = pk)
    subquery = Result.objects.filter(subject__id=pk, user=OuterRef('user')).order_by('-percent')
    results = Result.objects.filter(pk__in=Subquery(subquery.values('pk')[:1])).order_by('percent')
    form = QuestionForm()

    return render(request, 'subject.html', {'subject': subject, 'results':results, 'form':form})


@login_required
def quiz(request, pk):
    user = request.user
    subject = Subject.objects.get(id = pk)
    questions = Question.objects.filter(subject = subject)

    if request.method != 'POST':

        context = {
            'questions':questions,
            'subject':subject
        }

        return render(request, 'quiz.html', context)
    
    else:
        total = 0
        correct = 0


        for q in questions:
            total += 1
            if q.answer == request.POST.get(q.question):
                correct += 1
        
        try:
            percent = (correct/total)*100
        except ZeroDivisionError:
            percent = 0

        new_result = Result(
            user = user,
            subject = subject,
            total = total,
            correct = correct,
            percent = percent
        )
        new_result.save()

        results = Result.objects.filter(subject__id = pk)

        context = {
            'total': total,
            'correct': correct,
            'subject': subject,
            'results': results
        }      
        
        return render(request, 'result.html', context)
    

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    template_name = 'subject_new.html'
    fields = ['name']


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subject_delete.html'
    success_url = reverse_lazy('subjects')


@login_required
def add_question(request, pk):
    subject = Subject.objects.get(id = pk)
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.subject = subject
            new_question.save()

            return redirect('subject_edit', pk=pk)
        
        
    context = {
        'subject':subject,
        'form':form,
    }
    return render(request, 'subject_edit.html', context)


def subject_edit(request, pk):
    subject = Subject.objects.get(id=pk)
    questions = Question.objects.filter(subject__id = pk)
    form = QuestionForm()

    context = {
        'questions': questions,
        'subject': subject,
        'form':form
    }
    
    return render(request, 'subject_edit.html', context)


def delete_question(request, pk):
    question = Question.objects.get(id = pk)
    question.delete()

    return redirect(request.META.get('HTTP_REFERER', 'subjects'))



