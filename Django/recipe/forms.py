from .models import Recipe
from django import forms


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title',
                  'description_free_text',
                  'original_website_link',
                  'ingredients_free_text',
                  'instructions_free_text',
                  'servings_per_nominal']
        labels = {
            "title": "Recipe Title",
            "original_website_link": "Original Website Link",
            "description_free_text": "Recipe Description",
            "ingredients_free_text": "Recipe Ingredients",
            "instructions_free_text": "Recipe Instructions",
            "servings_per_nominal": "Individual Servings",
        }
