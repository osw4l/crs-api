from datetime import datetime


class DateParamConverter:
    """
        Class converter to validate date params from urls because is not supported yet
    """
    regex = r'\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)

