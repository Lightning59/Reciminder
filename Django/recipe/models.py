from django.db import models
import uuid6


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7(), unique=True, editable=False)
    title=models.CharField(max_length=255) # this seemed pretty long based on my attempts to type up a hypothetical
                                           # long recipe title - Came to ~100. So pick 255(256?) as a good permissive lim
    description_free_text=models.TextField(null=True, blank=True)
    ingredients_free_text=models.TextField(null=True, blank=True)
    instructions_free_text=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    deleted_by_user=models.BooleanField(default=False)
    servings_per_nominal=models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created']
