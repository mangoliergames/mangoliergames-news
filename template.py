"""
Copyright 2025 Mangolier Games

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class Template(object):
    """
    Stores a template in text format and provides a method to format the
    template with a list of kwargs. Dictionary keys should match tokens in
    the template to the desired values
    """
    @classmethod
    def fromFile(cls, path):
        """
        Creates a Template from a file path on disk
        """
        with open(path, 'r') as f:
            return cls(f.read())

    def __init__(self, template):
        """
        Creates a Template from a string
        """
        self.__template = template

    def format(self, **kwargs):
        """
        Fills all {{{TOKEN}}} entries in the template with the key/value
        pair from kwargs that matches the TOKEN name
        """
        formatted = self.__template

        for key, value in kwargs.items():
            token = '{{{{{{{}}}}}}}'.format(key)
            formatted = formatted.replace(token, str(value))

        return formatted
