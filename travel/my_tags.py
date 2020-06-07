from django import template
register = template.Library()

@register.filter(name='times')
def times(number):
    if number:
        return range(number)
    return number

@register.filter(name='get_int')
def get_int(number):
    return int(number)
@register.filter(name='add_one')
def get_int(number):
    return ++number

@register.filter(name='get_float')
def get_float(number):
    if number:
        while number>=1:
            number -=1;
    return number