from django.contrib import admin
from .models import Subject, Question, Result


admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Result)