from django import template
import math

register = template.Library()

@register.filter(name='range')
def create_range(min,max):
    return range(min,max+1)

@register.filter(name='starrange')
def booklistrange(review_obj):
    if review_obj.count()!=0:
        avg=0.0
        for obj in review_obj:
            avg+=int(obj.star_rating)
        average=round(avg/review_obj.count(),1)
        average_int=round(math.floor(average))
        return range(1,average_int+1)       
    else:
        return ''
