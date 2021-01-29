from django.db import models


class Profiles(models.Model):
    profileNo = models.CharField(max_length=100)
    eyeColor = models.CharField(max_length=250)
    haircolor = models.CharField(max_length=250)
    profileAge = models.CharField(max_length=20)
    profileUsername = models.CharField(max_length=20)
    profileDesc = models.TextField()

    def __str__(self):
        return str(self.profileNo)+'- '+self.profileUsername
    
    