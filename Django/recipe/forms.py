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
                  'servings_per_nominal',
                  'nutrition_free_text',
                  'notes_free_text',
                  'pre_prep_active_time_minutes',
                  'prep_active_time_minutes',
                  'cook_active_time_minutes',
                  'clean_active_time_minutes',
                  'pre_prep_passive_time_minutes',
                  'cook_passive_time_minutes',
                  'after_cook_passive_time_minutes',
                  ]
        labels = {
            "title": "Recipe Title",
            "original_website_link": "Original Website Link",
            "description_free_text": "Recipe Description",
            "ingredients_free_text": "Recipe Ingredients",
            "instructions_free_text": "Recipe Instructions",
            "servings_per_nominal": "Individual Servings",
            'nutrition_free_text': "Nutrition",
            'notes_free_text': "Notes",
            'pre_prep_active_time_minutes': 'Active Pre-Prep (Preparing marinade etc.)',
            'prep_active_time_minutes' : 'Active Prep (Right before cooking/serving)',
            'cook_active_time_minutes': 'Active Cook (Cook time with frequent hands on)',
            'clean_active_time_minutes': 'Post Cook time, Cleaning etc',
            'pre_prep_passive_time_minutes': 'Passive pre-prep (Time spent marinading overnight in the fridge etc)',
            'cook_passive_time_minutes' : 'Any Passive Cooking Time (Baking in the oven for 2 hours)',
            'after_cook_passive_time_minutes': 'Passive after cook time (Rest period or Ice cream chilling in freezer).',
        }
