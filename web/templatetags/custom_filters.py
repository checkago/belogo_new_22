from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def highlight(text, query):
    highlighted_text = text.replace(query, f'<span class="bg-primary font-weight-bold">{query}</span>')
    return mark_safe(highlighted_text)