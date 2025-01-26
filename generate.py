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

import argparse
import os

from post import Post
from template import Template

def generate_posts(
            post_template,
            index_template,
            index_entry_template,
            input_path,
            output_path):

    # Ensure the output directory always exists
    os.makedirs(output_path, exist_ok=True)

    post_template = Template.fromFile(post_template)
    posts = []

    # For each directory in the input path, attempt to load a post
    # configuration from the contents of the directory
    for path in os.listdir(input_path):
        input_root = os.path.abspath(os.path.join(input_path, path))
        full_path = os.path.join(os.path.basename(output_path), path)

        print("Processing '{}', path='{}'".format(input_root, full_path))

        # Error if there's a stray file in the input directory
        if not os.path.isdir(input_root):
            print(" - Invalid post file '{}'".format(input_root))
            continue

        # Error if we fail to load a post from the directory
        post = Post.fromFile(input_root, full_path, path)
        if not post:
            print(" - Invalid post")
            continue

        # Generate the post
        output_root = os.path.abspath(os.path.join(output_path, path))
        os.makedirs(output_root, exist_ok=True)
        print(" - Generate posting in '{}'".format(output_root))

        post.write(post_template, output_root)
        posts.append(post)

    # Posts are sorted by their date, with latest first
    posts.sort(key=Post.key)
    
    # Generate index entries for all posts
    index_entry_template = Template.fromFile(index_entry_template)
    index_entries = []
    for post in posts:
        index_entries.insert(0, post.index(index_entry_template))

    # Generate the index
    index_format = {'ENTRIES': "".join(index_entries)}
    index_template = Template.fromFile(index_template)

    output_index = os.path.abspath(os.path.join(output_path, 'index.html'))
    with open(output_index, 'w') as f:
        f.write(index_template.format(**index_format))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--post-template",
        type=str,
        dest="post_template",
        required=True,
        help="The path to the news post template file")
    parser.add_argument(
        "--index-template",
        type=str,
        dest="index_template",
        required=True,
        help="The path to the index page template file")
    parser.add_argument(
        "--index-entry-template",
        type=str,
        dest="index_entry_template",
        required=True,
        help="The path to the index page entry template file")
    parser.add_argument(
        "--posts",
        type=str,
        dest="posts",
        required=True,
        help="The path to the folder that contains posts to parse")
    parser.add_argument(
        "--output",
        type=str,
        dest="output",
        required=True,
        help="The path to the folder that contains the generated output")

    args = parser.parse_args()
    generate_posts(
        args.post_template,
        args.index_template,
        args.index_entry_template,
        args.posts,
        args.output)
