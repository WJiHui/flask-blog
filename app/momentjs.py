# encoding:utf-8
from jinja2 import Markup
from flask_babel import format_datetime


class Momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = format_datetime(timestamp)
        # self.timestamp = timestamp

    def render(self, format):
        # return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))
        # return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>"
                      # % (self.timestamp, format))
        return self.timestamp

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
