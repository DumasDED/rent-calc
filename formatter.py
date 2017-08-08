import string


class NegativeParenFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        try:
            if value < 0:
                return "(" + string.Formatter.format_field(self, -value, format_spec) + ")"
            else:
                return string.Formatter.format_field(self, value, format_spec)
        except:
            return string.Formatter.format_field(self, value, format_spec)