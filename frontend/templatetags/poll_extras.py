from django import template

register = template.Library()


@register.filter(name='remove_zero')
def mul(val):
    try:
        return int(val)
    except ValueError:
        val = val.split(',')[0]
        val = val.split('.')[0]
        return val


@register.filter(name='to_int')
def to_int(val):
    try:
        return int(val)
    except:
        return val


@register.filter(name='to_str')
def to_str(val):
    try:
        return str(val)
    except:
        return val
