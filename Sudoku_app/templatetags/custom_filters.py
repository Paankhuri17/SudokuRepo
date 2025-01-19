from django import template

register = template.Library()

@register.filter
def divide(value, divisor):
    try:
        return int(value / divisor)
    except (TypeError, ZeroDivisionError):
        return 0  # Return 0 or a fallback value for invalid division


@register.simple_tag(takes_context=True)
def increment_counter(context, key, increment_by=1):
    """
    Increments a variable in the template context by a specified value.

    :param context: The template context (auto-passed)
    :param key: The name of the variable to increment
    :param increment_by: The value to increment by (default: 1)
    :return: The updated counter value
    """
    if key not in context:
        context[key] = 0  # Initialize if not already in context
    context[key] += increment_by
    return context[key]
