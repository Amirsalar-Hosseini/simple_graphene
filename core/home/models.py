from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name



class Car(models.Model):
    person = models.ManyToManyField(Person)
    name = models.CharField(max_length=100)
    year = models.IntegerField()


    def __str__(self):
        return self.name
