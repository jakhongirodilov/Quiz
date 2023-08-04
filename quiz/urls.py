from django.urls import path
from .views import home, subject, SubjectDeleteView, SubjectCreateView, add_question, quiz, subject_edit, delete_question


urlpatterns = [
    path('', home, name='subjects'),
    path('quiz/<int:pk>', quiz, name='quiz'),
    path('<int:pk>/', subject, name='subject'),
    path('new/', SubjectCreateView.as_view(), name='subject_new'),
    path('subject_edit/<int:pk>/', subject_edit, name='subject_edit'),
    path('subject_delete/<int:pk>', SubjectDeleteView.as_view(), name='subject_delete'),
    path('add_question/<int:pk>', add_question, name='add_question'),
    path('delete_question/<int:pk>/', delete_question, name='question_delete')
]

