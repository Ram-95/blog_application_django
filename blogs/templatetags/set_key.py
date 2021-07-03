from django import template
register = template.Library()
"""This is custom filter to extract key value from a Dictionary. 
This feature is not provided as part of Django Template Language
So writing our own template function to achieve this.

- This file should reside in a directory called 'templatetags' along with '__init__.py'
Reference: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/

To Use this filter: {{ <set_name|set_key:<key to search> }}
"""

@register.filter(name='set_key')
def get_item(set, key):
    '''Returns the given key from a set.'''
    return key in set
        
    