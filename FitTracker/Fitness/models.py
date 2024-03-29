from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    class Meta:
        db_table = "Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, null=False, default='O')
    dob = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    target_calorie_intake = models.FloatField(default=0)
    target_calorie_burn = models.FloatField(default=0)
    target_carbohydrate_intake = models.FloatField(default=0)
    target_protein_intake = models.FloatField(default=0)
    target_fat_intake = models.FloatField(default=0)
    target_water_intake = models.FloatField(default=0)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            # user conditional statements to add more options 
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()




class TargetsHistory(models.Model):
    class Meta:
        db_table = "TargetsHistory"
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    target_type = models.CharField(max_length=40,null=False)
    target_value = models.FloatField()
    created_on = models.DateTimeField(default = timezone.now)    

class Measurements(models.Model):
    class Meta:
        db_table = "Measurements"
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    waist = models.FloatField(null=True)
    hip = models.FloatField(null=True)
    bmi = models.FloatField(null=True)
    waist_hip_ratio = models.FloatField(null=True)
    waist_height_ratio = models.FloatField(null=True)

class Food(models.Model):
    class Meta:
        db_table = "Food"
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50, unique=True, null=False)
    carbs_per_serving = models.FloatField(null=False)
    cal_per_serving = models.FloatField(null=False)
    pro_per_serving = models.FloatField(null=False)
    fat_per_serving = models.FloatField(null=False)

class FoodLog(models.Model):
    class Meta:
        db_table = "FoodLog"
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #food = models.ForeignKey(Food, null=False, on_delete=models.CASCADE)
    food_id = models.IntegerField(null=False)
    food_name = models.CharField(max_length=50,null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    quantity = models.IntegerField(null=False)
    calories = models.FloatField(null=False)
    proteins = models.FloatField(null=False)
    fat = models.FloatField(null=False)
    carbs = models.FloatField(null=False)


class Exercise(models.Model):
    class Meta:
        db_table = "Exercise"
    name = models.CharField(max_length=50, unique=True, null=False)
    url = models.URLField(null=False)
    cal_burned_per_min = models.FloatField(null=False)

class ExerciseLog(models.Model):
    class Meta:
        db_table = "ExerciseLog"
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    duration = models.IntegerField(null=False)  




