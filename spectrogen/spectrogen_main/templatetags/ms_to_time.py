from django import template
register = template.Library()

@register.filter()
def mstotime(milliseconds):
    seconds = int(int(milliseconds) / 1000)
    minutes = int(int(seconds) / 60)
    hours = int(int(minutes) / 60)

    final_time_string = str(seconds) + 's'
    if minutes > 0:
        final_time_string = str(minutes) + 'm' + final_time_string
        if hours > 0:
            final_time_string = str(hours) + 'h' + final_time_string

    return final_time_string

@register.filter()
def mstosec(milliseconds):
    return str(int(milliseconds / 1000))