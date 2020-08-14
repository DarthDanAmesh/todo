from django.db import models

# Create your models here.
STATUS = ((0,'Active'),(1,'Completed'),(2,'Due Date Passed'))

class ToDo(models.Model):
    item = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    date_assigned = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.IntegerField(STATUS, default=0)

    class Meta:
        ordering = ['-date_assigned']

    def __str__(self):
        return self.item
        


