from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
	name = models.CharField(max_length=200)
	src = models.CharField(max_length=100, default="src")
	dest = models.CharField(max_length=100, default="dest")

	def __str__(self):
		return self.name

class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text

class Search(models.Model):
	search = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.search)

	class Meta:
		verbose_name_plural = 'Searches'