from django import template

from pytz import timezone

register = template.Library()

import iso8601 as iso8601lib

# Thank you: http://djangosnippets.org/snippets/1039/
def dequote(args):
    "Given a list, will return a list with any leading and trailing quotes from the items in the list removed"
    return [ ( arg[1:-1] if arg[0] == arg[-1] and arg[0] in ('"', "'") else arg ) for arg in args ]

@register.tag
def iso8601(parser, token):
    usage = "tag usage: {%% %r date_str display_format %%}"
    try:
        tag_name, args = token.contents.split(None, 1)
        args_list = args.split()
        iso8601_datestr, timezone, format = args_list[0], args_list[1], args_list[2]
    except:
        pass
        
    return ISO8601Node(iso8601_datestr, timezone, "".join(dequote(format)))


class ISO8601Node(template.Node):
    def __init__(self, datestr, tz, format):
        super(ISO8601Node, self).__init__()
        self.datestr = template.Variable(datestr)
        self.timezone = template.Variable(tz)
        self.format  = format

    def render(self, context):
        datestr = self.datestr.resolve(context)
        tz      = self.timezone.resolve(context)

        utcdate = iso8601lib.parse_date(datestr)
        timezonedate = utcdate.astimezone(timezone(tz))
        return timezonedate.strftime(self.format)
