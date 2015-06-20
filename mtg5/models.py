from django.db import models

# Represents a card
class Card(models.Model):
	name = models.CharField(max_length=50)
	setName = models.CharField(max_length=3)
	number = models.IntegerField()
	def __unicode__(self):
		return self.name + " (" + self.setName + ")"

