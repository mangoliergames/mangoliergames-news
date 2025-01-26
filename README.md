# About
Static site generator for the [Mangolier Games news posts](https://www.mangoliergames.com/news) index and pages. Generates .html files and an index from a directory contain posts, which are defined using a configuration file, a markdown text file, and any extra files like images.

## Dependencies

The generator depends on two Python packages, which need to be installed in the Python environment used to run the `generate.py` script. Both packages can be installed using `pip`.

* [dateutil](https://github.com/dateutil/dateutil) provides parsing of date strings without the need to specify a format, for automatic ordering of pages
* [marko](https://github.com/frostming/marko) is used to generate HTML from a post's Markdown text file

## Using the Generator
The generator can be used by running the `generate.py` script with the appropriate arguments. All arguments are required:

```
  --post-template           The path to the news post template file
  --index-template          The path to the index page template file
  --index-entry-template    The path to the index page entry template file
  --posts                   The path to the directory that contains posts to parse
  --output                  The path to the directory to write outputs to
```

For example, to run the generator on the sample templates and input pages supplied in this repository:

```
python3 generate.py --post-template templates/post.tmpl --index-template templates/index.tmpl --index-entry-template templates/index_entry.tmpl --posts examples --output outputs
```

## Input Folder Structure
Each post is defined as its own directory in the `posts` input folder. Each post folder must contain a `post.cfg` with three lines that define the title, date, and tag for the post. It must also contain a `post.txt` file that contains the post text formatted using Markdown. Any additional in the post directory are copied as-is from the input folder to the generated output folder.

Input:
```
examples/
├── example-1
│   ├── image.png
│   ├── post.cfg
│   └── post.txt
├── example-2
│   ├── post.cfg
│   └── post.txt
```

Output:
```
outputs/
├── example-1
│   ├── image.png
│   └── index.html
├── example-2
│   └── index.html

```

## Templating
The site generator use a simple template system that uses a partially complete .html file with special `{{{TOKENS}}}` that are replaced during static generation. Sample plain text template are provided in the `templates` directory. In practice you'll want to define your page and index templates so they include any custom CSS, font resources, favicons, etc.

### Post template
The post template supports the following tokens, which are loaded from the post configuration file:
* `TITLE` -- The post title.
* `DATE` -- The date the post was published.
* `TAG` -- A custom tag string for the post.
* `BODY` -- The parsed markdown body text for the post.

### Index template
The index template supports a single token, which is an HTML blob generated internally applying the *Index Entry Template* for each detected post:
* `ENTRIES` -- The HTML blob that defines the list of post entries.

### Index Entry Template
A partial template the specifies what the index entry HTML blob should look like for a single post. Supports the following tokens:
* `TITLE` -- The post title
* `DATE` -- The date the post was published.
* `TAG` -- A custom tag string for the post.
* `PATH` -- The full path to the post, including the output directory. For example, `posts/example-1`.
* `SLUG` -- The path of the post inside of the output directory. For example, `example-1`.

## License

This project is licensed under the MIT License.
