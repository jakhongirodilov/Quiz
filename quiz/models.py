from django.db import models
from django.urls import reverse
from accounts.models import CustomUser


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("subject", kwargs={"pk": self.pk})


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) 
    question = models.CharField(max_length=500)
    opt1 = models.CharField(max_length=200)
    opt2 = models.CharField(max_length=200)
    opt3 = models.CharField(max_length=200)
    opt4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.question    
    

class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total = models.IntegerField()
    correct = models.IntegerField()
    percent = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.subject} | {self.user}"

