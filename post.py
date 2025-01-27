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

import dateutil.parser
import marko
import os
import shutil

class Post(object):
    """
    Stores the configuration data and text used to generate a post
    """

    _CONFIG_FILE_NAME = "post.cfg"
    _TEXT_FILE_NAME = "post.txt"

    @classmethod
    def fromFile(cls, root, path, slug):
        """
        Constructs a post object from a root file path
        """

        # Parse the config file to find the title, date, and tag
        config_path = os.path.join(root, cls._CONFIG_FILE_NAME)
        if not os.path.isfile(config_path):
            print(" - Post dir '{}' is missing a 'post.cfg' file".format(root))
            return None

        with open(config_path, 'r') as f:
            lines = f.readlines()
            num_lines = len(lines)

            if num_lines < 3 or num_lines > 4:
                print(" - Config '{}' must have 3 or 4 lines".format(
                    config_path))
                return None

            title = lines[0].rstrip()
            date = lines[1].rstrip()
            tag = lines[2].rstrip()

            if num_lines == 4:
                desc = lines[3].rstrip()
            else:
                desc = ""

        # Parse the main post markdown file
        text_path = os.path.join(root, cls._TEXT_FILE_NAME)
        if not os.path.isfile(text_path):
            print(" - Post dir '{}' is missing a 'post.txt' file".format(root))
            return None

        with open(text_path, 'r') as f:
            text = f.read()
            text = marko.convert(text)

        # Any extra files are copied as-is
        extra_files = []
        for file in os.listdir(root):
            if file == cls._CONFIG_FILE_NAME:
                continue
            if file == cls._TEXT_FILE_NAME:
                continue
            extra_files.append(os.path.join(root, file))

        return cls(path, slug, title, date, desc, tag, text, extra_files)

    @staticmethod
    def key(post):
        return post.__parsed_date

    def __init__(self, path, slug, title, date, desc, tag, text, extra_files):
        """
        Constructs a post from various configuration options
        """
        self.__path = path
        self.__slug = slug

        self.__title = title
        self.__date = date
        self.__parsed_date = dateutil.parser.parse(self.__date)
        self.__desc = desc
        self.__tag = tag

        self.__text = text
        self.__extra_files = extra_files

    def index(self, template):
        """
        Generates an index page HTML segment for this page using the 
        specified index entry template
        """
        parameters = {
            'TITLE': self.__title,
            'DESC': self.__desc,
            'TAG' : self.__tag,
            'DATE' : self.__date,
            'PATH' : self.__path,
            'SLUG' : self.__slug
        }

        return template.format(**parameters)

    def write(self, template, output):
        """
        Generates an HTML post from this instance using the specified
        template and writes it to the output directory. Any extra files
        are also copied into the same location.
        """
        parameters = {
            'TITLE': self.__title,
            'DESC': self.__desc,
            'TAG' : self.__tag,
            'DATE' : self.__date,
            'BODY' : self.__text,
            'PATH' : self.__path,
            'SLUG' : self.__slug,
        }
        text = template.format(**parameters)

        # Write out the main index.html file the post by formatting the 
        # template using the various fields parsed from the config and
        # the generated body text
        post_path = os.path.join(output, 'index.html')
        with open(post_path, 'w') as f:
            print(" - Writing post to '{}'".format(post_path))
            f.write(text)

        # Copy extra-files as is to the post directory
        for extra_file in self.__extra_files:
            dst = os.path.basename(extra_file)
            dst = os.path.join(output, dst)
            
            print(" - Copying extra file '{}'".format(extra_file))
            shutil.copyfile(extra_file, dst)
