from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class ProfileSerialzer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile
        fields = ('__all__')

    def _kgToPound(self, kg):
        return kg * 2.205
    
    def _poundToKg(self, pound):
        return pound / 2.205

    def update(self, instance, validated_data):
        weight = self._kgToPound(validated_data.get('weight', instance.weight))
    
        instance.gender = validated_data.get("gender", instance.gender)
        instance.dob = validated_data.get("dob", instance.dob)

        instance.weight = validated_data.get("weight", instance.weight)
        instance.height = validated_data.get("height", instance.height)

        instance.target_calorie_intake = validated_data.get("target_calorie_intake", instance.target_calorie_intake)
        instance.target_calorie_burn = validated_data.get("target_calorie_burn", instance.target_calorie_burn)
        instance.target_carbohydrate_intake = validated_data.get("target_carbohydrate_intake", instance.target_carbohydrate_intake)
        instance.target_protein_intake = validated_data.get("target_protein_intake", instance.target_protein_intake)
        instance.target_fat_intake = validated_data.get("target_fat_intake", instance.target_fat_intake)
        instance.target_water_intake = weight * 0.5 # in ounce

        instance.save()
        return instance

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], first_name = validated_data["first_name"] , last_name = validated_data["last_name"])
        return user
#TODO change the below 2 serializer to one
class FoodLogSerializerGet(serializers.ModelSerializer):
    #food_name = serializers.CharField(source='food.name',read_only=True)
    class Meta:
        model = FoodLog
        fields = '__all__'
        #fields = ['id', 'date', 'quantity', 'user_profile', 'food_name','food_id']
    
class FoodLogSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = '__all__'

class ExerciseLogSerializerGet(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name',read_only=True)
    url = serializers.URLField(source='exercise.url',read_only=True)
    cal_burned_per_min = serializers.FloatField(source='exercise.cal_burned_per_min',read_only=True)
    class Meta:
        model = ExerciseLog
        fields = ['id', 'user_profile', 'exercise_id' ,'exercise_name', 'date' , 'duration', 'url', 'cal_burned_per_min']

class ExerciseLogSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

class MeasurementsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = '__all__'