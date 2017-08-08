import string


class NegativeParenFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        try:
            if value < 0:
                if format_spec.startswith('$'):
                    return "($" + string.Formatter.format_field(self, -value, format_spec[1:]) + ")"
                else:
                    return "(" + string.Formatter.format_field(self, -value, format_spec[1:]) + ")"
            else:
                if format_spec.startswith('$'):
                    return "$" + string.Formatter.format_field(self, value, format_spec[1:])
                else:
                    return string.Formatter.format_field(self, value, format_spec[1:])
        except:
            return string.Formatter.format_field(self, value, format_spec)
