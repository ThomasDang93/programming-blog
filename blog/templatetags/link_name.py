from django import template
import re

register = template.Library()


@register.filter(name='link_name')
def link_name(path, page_number):
    output = re.search('(page=\d+)', path)
    if output is not None:
        print(str(output.group(1)))
        return path.replace(str(output.group(1)), "page={}".format(page_number))
    if re.search('(page=\d+)', path):
        path.replace()
    page_number = str(page_number)
    if '?' in path:
        return path + "&page=" + page_number
    return path + "?page=" + page_number
