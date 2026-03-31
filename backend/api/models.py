from django.db import models
from django.contrib.auth.models import User

class RecipeManager(models.Manager):
    def by_category(self, category_name):
        return self.filter(category__name=category_name)

    def recent(self):
        return self.order_by('-created_at')[:10]

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    objects = RecipeManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"

class MealPlan(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plan')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plan')

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"

    class Meta:
        unique_together = ('user', 'date', 'meal_type')
        ordering = ['date']
