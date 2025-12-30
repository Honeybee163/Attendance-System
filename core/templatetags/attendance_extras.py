from django import template

register = template.Library()

@register.filter
def percentage(attended, total):
    try:
        return round((attended / total) * 100, 1)
    except (ZeroDivisionError, TypeError):
        return 0
