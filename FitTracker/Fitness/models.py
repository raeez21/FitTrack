from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, null=False, default='O')
    dob = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    targetCalorieIntake = models.FloatField(default=0)
    targetCalorieBurn = models.FloatField(default=0)
    targetCarbohydrateIntake = models.FloatField(default=0)
    targetProteinIntake = models.FloatField(default=0)
    targetFatIntake = models.FloatField(default=0)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            # user conditional statements to add more options 
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

    
class Measurements(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    height = models.FloatField()
    weight = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()
    bmi = models.FloatField()
    waist_hip_ratio = models.FloatField()
    waist_height_ratio = models.FloatField()

class Food(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    carbs_per_serving = models.FloatField(null=False)
    cal_per_serving = models.FloatField(null=False)
    pro_per_serving = models.FloatField(null=False)
    fat_per_serving = models.FloatField(null=False)

class FoodLog(models.Model):  
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    quantity = models.IntegerField(null=False)  

class Exercise(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    url = models.URLField(null=False)
    cal = models.FloatField(null=False)

class ExerciseLog(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    duration = models.IntegerField(null=False)  




