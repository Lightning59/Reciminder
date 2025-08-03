from django import template
import recipe.utils

register = template.Library()

@register.simple_tag
def pretty_time_print(minutes, long):
    return recipe.utils.minutes_to_user_text(minutes,long)