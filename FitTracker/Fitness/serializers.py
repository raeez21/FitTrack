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

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = '__all__'
