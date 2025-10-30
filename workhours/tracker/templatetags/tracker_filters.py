from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='format_hours')
def format_hours(value):
    """
    Format decimal hours into a readable format.
    Example: 1.50 -> 1:30
    """
    if not value:
        return "0:00"
    
    try:
        # Convert to decimal and round to 2 decimal places
        value = Decimal(str(value)).quantize(Decimal("0.01"))
        # Get the whole hours
        hours = int(value)
        # Get the remaining minutes (e.g., 0.5 hours = 30 minutes)
        minutes = int((value - hours) * 60)
        return f"{hours}:{minutes:02d}"
    except (ValueError, TypeError, AttributeError):
        return "0:00"

@register.filter(name='format_decimal_hours')
def format_decimal_hours(value):
    """
    Format decimal hours with 2 decimal places.
    Example: 5.83000000000000 -> 5.83
    """
    if not value:
        return "0.00"
    
    try:
        # Convert to decimal and round to 2 decimal places
        value = Decimal(str(value)).quantize(Decimal("0.01"))
        return str(value)
    except (ValueError, TypeError, AttributeError):
        return "0.00"