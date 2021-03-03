from django import template
register = template.Library()

@register.filter(name='perc')
def perc(value):
    """
    Formats a float to be represented as a percantage.
    """
    return f'{value:0.2%}'
