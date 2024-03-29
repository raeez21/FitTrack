from rest_framework import serializers
from .models import *
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core import validators

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
        print("hereee")
        # weight = self._kgToPound(validated_data.get('weight', instance.weight))
    
        # instance.gender = validated_data.get("gender", instance.gender)

        # instance.dob = validated_data.get("dob", instance.dob)

        # instance.weight = validated_data.get("weight", instance.weight)
        # instance.height = validated_data.get("height", instance.height)

        # instance.target_calorie_intake = validated_data.get("target_calorie_intake", instance.target_calorie_intake)
        # instance.target_calorie_burn = validated_data.get("target_calorie_burn", instance.target_calorie_burn)
        # instance.target_carbohydrate_intake = validated_data.get("target_carbohydrate_intake", instance.target_carbohydrate_intake)
        # instance.target_protein_intake = validated_data.get("target_protein_intake", instance.target_protein_intake)
        # instance.target_fat_intake = validated_data.get("target_fat_intake", instance.target_fat_intake)
        # instance.target_water_intake = weight * 0.5 # in ounce

        #instance.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
        #return instance

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        ##AYUSH user = serializers.CurrentUserDefault().user
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        password_validation.validate_password(data['new_password'], serializers.CurrentUserDefault())
        return data
    # def validate_new_password(self, value):
    #     #validate_password(value)
    #     password_validation.validate_password(value, serializers.CurrentUserDefault(), password_validators=[
    #          validators.MinLengthValidator(4), # Allow shorter passwords
    #      ])
    #     return value
    #     # try:
        #     print("new:", value)
        #     password_validation.validate_password(value, password_validators=[], min_length=4)
        # except password_validation.ValidationError as error:
        #     # Raise a custom validation error message
        #     raise serializers.ValidationError({'new_password': error.messages})

        # return value
        # "#return value
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    

    # def save(self, **kwargs):
    #     password = self.validated_data['new_password1']
        
    #     user = serializers.CurrentUserDefault()
    #     user.set_password(password)
    #     user.save()
    #     return user
    

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
    cal_burned = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ExerciseLog
        fields = ['id', 'user_profile', 'exercise_id' ,'exercise_name', 'date' , 'duration', 'url', 'cal_burned_per_min','cal_burned']
    def get_cal_burned(self, obj):
        return obj.duration * obj.exercise.cal_burned_per_min

class ExerciseLogSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

class MeasurementsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = '__all__'