from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='time_elapsed')
def time_elapsed(value):
    print(value)
    print(type(value))
    print(datetime.now())
    time = datetime.now() - value
    time = time.total_seconds() / 60
    if time < 60:
        time = f'{int(time)} mins'
    elif 60 <= time <= 1439:
        time = f'{int(time/60)} hours'
    else:
        time = f'{int(time/60/24)} days'
    return time
