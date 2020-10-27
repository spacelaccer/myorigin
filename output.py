from io import StringIO


class ShellOutput():

    _buffer = StringIO()
    _format = []

    @classmethod
    def renew(cls):
        cls._buffer.seek(0)
        cls._buffer.truncate()
        cls._format.clear()

    @classmethod
    def append(cls, output, format_string):
        new_format = []
        new_format.append(len(cls._buffer.getvalue()))
        cls._buffer.write(output)
        new_format.append(len(cls._buffer.getvalue()))
        new_format.append(format_string)
        cls._format.append(new_format)

    @classmethod
    def newline(cls, count=1):
        cls._buffer.write('\n'*count)

    @classmethod
    def flush(cls):
        cls._buffer.write('\n')

    @classmethod
    def value(cls):
        return cls._buffer.getvalue()

    @classmethod
    def format(cls):
        return cls._format