from django.db import models

# Create your models here.

class QusAns(models.Model):
    # Can gice phone nnumbers in data, name
    #  attach with candidate model
    QA = models.TextField()
    phone = models.CharField(max_length=50)
