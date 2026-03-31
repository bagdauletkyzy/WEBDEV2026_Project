from rest_framework import serializers
from .models import Recipe, MealPlan, Ingredient
from django.contrib.auth.models import User

class RecipeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class MealPlanModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class IngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    quantity = serializers.DecimalField(max_digits=6, decimal_places=2)
    unit = serializers.CharField(max_length=50)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), source='recipe', write_only=True
    )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.recipe = validated_data.get('recipe', instance.recipe)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
