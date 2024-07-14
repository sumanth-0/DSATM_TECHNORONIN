from django.db import models

# Create your models here.
class Url_table(models.Model):
    url_input = models.CharField(max_length=200)
    
    def __str__(self):
        return self.url_input